"""
Signals a enviarse para la App Django.
"""
from django.dispatch import Signal

payment_successful = Signal()

payment_amount_error = Signal()

payment_receiver_id_error = Signal()
