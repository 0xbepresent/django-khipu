import mock

from django.test import TestCase

from ..models import Payment


class TestModels(TestCase):

    def test_payment(self):
        """
        Testing the Payment Model
        """
        p = Payment()
        # Test model unicode
        p.payment_id = 'testing'
        self.assertEqual('Orden de compra Khipu testing', p.__str__())

        # Test payment_successful signal
        p.status = 'done'
        with mock.patch('khipu.signals.payment_successful.send') as mock_payment_successful:  # noqa
            p.send_signals()
            self.assertTrue(mock_payment_successful.called)

        # Test payment_amount_error signal
        p.status = 'amount_error'
        with mock.patch('khipu.signals.payment_amount_error.send') as mock_payment_amount_error:  # noqa
            p.send_signals()
            self.assertTrue(mock_payment_amount_error.called)

        # Test payment_receiver_id_error signal
        p.status = 'receiver_error'
        with mock.patch('khipu.signals.payment_receiver_id_error.send') as mock_payment_receiver_id_error:  # noqa
            p.send_signals()
            self.assertTrue(mock_payment_receiver_id_error.called)
