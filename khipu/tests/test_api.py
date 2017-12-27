import mock

from django.conf import settings
from django.test import TestCase

from ..api import Khipu
from ..exceptions import KhipuError


class TestAPI(TestCase):

    def test_khipu_service(self):
        """
        Testing de Khipu API.
        """
        # Test para cuando el servicio no existe.
        khipu = Khipu()
        with self.assertRaises(KhipuError):
            khipu.service('testing')

        # Test para cuando no existen variables settings.
        with self.assertRaises(KhipuError):
            settings.KHIPU_RECEIVER_ID = None
            khipu.service('GetBanks')
        settings.KHIPU_RECEIVER_ID = '148653'

        # Test para cuando todo esta OK con el servicio.
        with mock.patch(
            'khipu.services.common.KhipuService.request'),\
                mock.patch(
                'khipu.services.common.KhipuService.response',
                return_value={'banks': 'testingbank'}):
            result = khipu.service('GetBanks')
            self.assertTrue('banks' in result)
