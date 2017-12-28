import mock

from django.test import TestCase

from ..exceptions import KhipuError
from ..forms import KhipuCreatePaymentForm


class TestForms(TestCase):

    def test_khipucreatepaymentform(self):
        """
        Test para el form que ayuda a crear un formulario Khipu para obener
        una orden de pago.
        """
        # Los campos amount y currency son necesarios.
        with self.assertRaises(KhipuError):
            KhipuCreatePaymentForm(**{})

        # La conexion no se puede hacer con Khipu.
        with mock.patch('khipu.services.common.KhipuService.request'):
            f = KhipuCreatePaymentForm(**{
                'amount': 1000, 'currency': 'CLP', 'subject': 'my subject'})
            self.assertIsNone(f.payment_url)
            self.assertIsNone(f.transfer_url)
            self.assertIn("Servicio no disponible", f.render())

        # La conexion se hizo correcta con Khipu se renderea el form.
        with mock.patch('khipu.services.common.KhipuService.request'),\
                mock.patch(
                    'khipu.services.common.KhipuService.response',
                    return_value={
                        'payment_url': 'https://testing.com/a',
                        'transfer_url': 'https://testings.com/b'}):
            f = KhipuCreatePaymentForm(
                **{'amount': 1000, 'currency': 'CLP', 'subject': 'my subject'})
            self.assertIn("id_khipu_form_banco", f.render())
            self.assertIn("id_khipu_form_transferencia", f.render())
