# -*- coding: utf-8 -*-
PAYMENT_STATUS = [
    ('pending', 'Pagador aún no paga'),
    ('veryfing', 'Se está verificando el pago'),
    ('done', 'El pago ya está confirmado'),
    ('amount_error', 'El pago tiene un monto que no es válido'),
    ('receiver_error', 'El pago tiene un receiver_id que no es válido'),
]

PAYMENT_STATUS_DETAIL = [
    ('pending', 'El pagador aún no comienza a pagar'),
    ('normal',
        'El pago fue verificado y cancelado por algún medio de pago estandar'),
    ('marked-paid-by-payer', 'El pagador declaró que no pagará'),
    ('marked-as-abuse',
        'El pagador declaró que no pagará y que el cobro fue no solicitado'),
    ('reversed',
        'El pago fue anulado por el comercio, dinero fue devuelto al pagador')
]

PAYMENT_METHOD = [
    ('regular_transfer', 'Transferencia normal'),
    ('simplified_transfer', 'Transferencia simplificada'),
    ('not_available',
        'Para un pago marcado como realizado por otro medio por el cobrador')
]
