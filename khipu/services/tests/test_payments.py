import mock

from django.test import TestCase

from ..payments import GetPayment


class TestPayments(TestCase):

    def test_getpayment(self):
        """
        Testing clase GetPayment. Nos ayuda a obtener la info the un pago khipu
        mediante un token que le enviamos
        """
        # No enviamos la notification_token, el request se hace pero no
        # obtenemos informacion response
        with mock.patch(
                'khipu.services.common.KhipuService.request'):
            g = GetPayment(
                receiver_id=1211, secret='asas22', service_name='GetPayment')
            self.assertDictEqual(g.response(), {})

        # Enviamos token, se recibe correctamente en la data.
        with mock.patch(
                'khipu.services.common.KhipuService.request'):
            g = GetPayment(
                receiver_id=1211,
                secret='asas22',
                service_name='GetPayment',
                **{'notification_token': '12311'})
            self.assertEqual(g.data['notification_token'], '12311')
