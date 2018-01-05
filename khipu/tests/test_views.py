import mock

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

from ..exceptions import KhipuError
from ..models import Payment


class TestViews(TestCase):

    def test_verificacion(self):
        # Test para cuando hay un error con la comunicacion del servicio.
        with mock.patch('khipu.api.Khipu.service') as mock_service:
            mock_service.side_effect = KhipuError('testing')
            response = self.client.post(reverse("khipu_verificacion"), data={})
            self.assertTrue(response.status_code == 400)

        # Test para cuando hay un error en el guardado del modelo.
        # El payment_id no existe
        with mock.patch('khipu.api.Khipu.service') as mock_service:
            mock_service.return_value = {}
            response = self.client.post(reverse("khipu_verificacion"), data={})
            self.assertTrue(response.status_code == 400)

        # Testear cuando el monto NO es el mismo
        Payment.objects.create(payment_id='payment_id_testing', amount=122222)
        with mock.patch('khipu.api.Khipu.service') as mock_service, \
                mock.patch('khipu.signals.payment_amount_error.send') as mock_signal_amount_error:  # noqa
            mock_service.return_value = {
                'payment_id': 'payment_id_testing',
                'amount': '2000',
            }
            response = self.client.post(
                reverse("khipu_verificacion"),
                data={'notification_token': '2122'})
            self.assertTrue(mock_signal_amount_error.called)
            self.assertTrue(response.status_code == 200)

        # Testear cuando el receiver_id no es el correcto
        Payment.objects.create(
            payment_id='payment_id_testing_2', amount='2000')
        with mock.patch('khipu.api.Khipu.service') as mock_service, \
                mock.patch('khipu.signals.payment_receiver_id_error.send') as mock_signal_receiver_error:  # noqa
            mock_service.return_value = {
                'payment_id': 'payment_id_testing_2',
                'amount': '2000',
                'receiver_id': 'asass'
            }
            response = self.client.post(
                reverse("khipu_verificacion"),
                data={'notification_token': '2122'})
            self.assertTrue(mock_signal_receiver_error.called)
            self.assertTrue(response.status_code == 200)

        # Test para cuando es OK, payment ok is called.
        with mock.patch('khipu.api.Khipu.service') as mock_service, \
                mock.patch('khipu.signals.payment_successful.send') as mock_payment_successful:  # noqa
            mock_service.return_value = {
                'payment_id': 'payment_id_testing_2',
                'amount': '2000',
                'receiver_id': settings.KHIPU_RECEIVER_ID,
                'status': 'done'
            }
            response = self.client.post(
                reverse("khipu_verificacion"),
                data={'notification_token': '2122'})
            self.assertTrue(mock_payment_successful.called)
            self.assertTrue(response.status_code == 200)
