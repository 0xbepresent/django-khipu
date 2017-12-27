# -*- coding: utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe

from .api import Khipu


class KhipuCreatePaymentForm(forms.Form):
    """
    Formulario de Khipu para pagar con el banco o transferencia.
    """
    def __init__(self, *args, **kwargs):
        khipu = Khipu()
        result = khipu.service('CreatePayment', **kwargs)
        self.payment_url = result['payment_url']
        self.transfer_url = result['transfer_url']

    def render(self):
        return mark_safe(u"""
            <form action="{}" method="GET">
                <input type="image" src="https://s3.amazonaws.com/static.khipu.com/buttons/2015/150x50-transparent.png" alt="Paga con tu banco" />
            </form>
            <form action="{}" method="GET">
                <input type="image" src="https://s3.amazonaws.com/static.khipu.com/buttons/2015/150x50-transfer-transparent.png" alt="Pago por transferencia" />
            </form>
            """.format(self.payment_url, self.transfer_url)  # noqa
        )
