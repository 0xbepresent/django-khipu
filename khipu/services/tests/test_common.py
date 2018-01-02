import hashlib
import hmac
import mock
import requests

from django.conf import settings
from django.test import TestCase
from requests.exceptions import RequestException, Timeout, ConnectionError

from ..common import KhipuService
from ...exceptions import KhipuError


class TestCommon(TestCase):

    def test_khipuservice(self):
        """
        Test para la funcion que ayuda a conectarse directamente con Khipu.
        """
        ks = KhipuService(
            receiver_id=settings.KHIPU_RECEIVER_ID,
            secret=settings.KHIPU_SECRET_KEY,
            service_name='Testing')

        # Test funcion do_hash
        concatenated = 'GET&https%3A%2F%2Fkhipu.com%2Fapi%2F2.0%2Ftesting%2F'
        with mock.patch(
                'khipu.services.common.KhipuService.concatenated',
                return_value=concatenated):
            calculated_hash = hmac.new(
                settings.KHIPU_SECRET_KEY,
                concatenated,
                hashlib.sha256).hexdigest()
            self.assertEqual(ks.do_hash(), calculated_hash)

        # Test funcion concatenated
        with mock.patch(
                'khipu.services.common.KhipuService.get_url_service',
                return_value='https://khipu.com/api/2.0/testing/'):
            ks.method = 'GET'
            ks.data = {'amount': '200', 'subject': 'Hola soy un testing'}
            self.assertEqual(
                ks.concatenated(),
                "GET&https%3A%2F%2Fkhipu.com%2Fapi%2F2.0%2Ftesting%2F&amount=200&subject=Hola%20soy%20un%20testing")  # noqa

        # Test para generar una URL service
        ks.api_url = 'miapiurl.com/'
        ks.path = 'mipath'
        self.assertEqual(ks.get_url_service(), 'miapiurl.com/mipath')

        # Test para funcion get_headers
        do_hash_value = 'misuperhash'
        with mock.patch(
                'khipu.services.common.KhipuService.do_hash',
                return_value=do_hash_value):
            self.assertEqual(
                ks.get_headers()['Authorization'],
                "{}:{}".format(settings.KHIPU_RECEIVER_ID, do_hash_value))

        # Test funcion request
        with self.assertRaises(KhipuError),\
                mock.patch.object(requests, 'request') as mock_requests:
            mock_requests.return_value.status_code = 400
            ks.request()

        with self.assertRaises(KhipuError),\
                mock.patch.object(requests, 'request') as mock_requests:
            mock_requests.side_effect = RequestException
            ks.request()

        with self.assertRaises(KhipuError),\
                mock.patch.object(requests, 'request') as mock_requests:
            mock_requests.side_effect = Timeout
            ks.request()

        with self.assertRaises(KhipuError),\
                mock.patch.object(requests, 'request') as mock_requests:
            mock_requests.side_effect = ConnectionError
            ks.request()

        # Test funcion response
        with mock.patch.object(requests, 'request') as mock_requests:
            mock_requests.return_value.status_code = 200
            mock_requests.return_value.json = mock.Mock(
                return_value={'url': 'value'})
            ks.request()
            self.assertEqual(ks.data_response['url'], 'value')
            self.assertEqual(ks.response()['url'], 'value')
