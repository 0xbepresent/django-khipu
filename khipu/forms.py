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
        self.payment_url = result.get('payment_url')
        self.transfer_url = result.get('transfer_url')

    def render(self):
        if self.payment_url and self.transfer_url:
            html = mark_safe(u"""
                <form id="id_khipu_form_banco" action="{}" method="GET">
                    <input type="image" src="https://s3.amazonaws.com/static.khipu.com/buttons/2015/150x50-transparent.png" alt="Paga con tu banco" />
                </form>
                <form id="id_khipu_form_transferencia" action="{}" method="GET">
                    <input type="image" src="https://s3.amazonaws.com/static.khipu.com/buttons/2015/150x50-transfer-transparent.png" alt="Pago por transferencia" />
                </form>
                """.format(self.payment_url, self.transfer_url)  # noqa
            )
        else:
            html = mark_safe("<p>Servicio no disponible.</p>")
        return html
