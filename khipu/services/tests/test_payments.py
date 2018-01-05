import mock

from django.test import TestCase

from ...exceptions import KhipuError
from ..payments import GetPayment, CreatePayment


class TestPayments(TestCase):

    def test_getpayment(self):
        """
        Testing clase GetPayment. Nos ayuda a obtener la info the un pago khipu
        mediante un token que le enviamos
        """
        # No enviamos la notification_token, es un campo requerido.
        with self.assertRaises(KhipuError):
            g = GetPayment(
                receiver_id=1211, secret='asas22', service_name='GetPayment')

        # Enviamos token, se recibe correctamente en la data.
        with mock.patch(
                'khipu.services.common.KhipuService.request'):
            g = GetPayment(
                receiver_id=1211,
                secret='asas22',
                service_name='GetPayment',
                **{'notification_token': '12311'})
            self.assertEqual(g.data['notification_token'], '12311')

    def test_createpayment(self):
        """
        Testing clase que nos ayuda a obtener una orden de compra con Khipu
        """
        # Testing campos necesarios. amount y currency.
        with self.assertRaises(KhipuError):
            CreatePayment(
                receiver_id=1211, secret='asas22',
                service_name='CreatePayment', **{})

        # Testing el valor Booleano, Khipu espera un string, ejemplo: true
        with mock.patch(
                'khipu.services.common.KhipuService.request'),\
                mock.patch(
                    'khipu.models.Payment.objects.create',
                    return_value=mock.Mock(return_value=True)):
            cp = CreatePayment(
                receiver_id=1211,
                secret='asas22',
                service_name='CreatePayment',
                **{
                    'amount': 1, 'currency': 'CLP',
                    'subject': 'mysubject', 'send_email': True})
            self.assertEqual(cp.data['send_email'], 'true')

        # Testing con todo ok, se crea el modelo Payment.
        with mock.patch(
                'khipu.services.common.KhipuService.request'),\
                mock.patch(
                    'khipu.models.Payment.objects.create') as mock_create:
            cp = CreatePayment(
                receiver_id=1211,
                secret='asas22',
                service_name='CreatePayment',
                **{'amount': 1, 'currency': 'CLP', 'subject': 'mysubject'})
            self.assertTrue(mock_create.called)
