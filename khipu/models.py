from django.db import models

from .constants import PAYMENT_STATUS, PAYMENT_STATUS_DETAIL, PAYMENT_METHOD
from .signals import (
    payment_successful, payment_amount_error, payment_receiver_id_error)


class Payment(models.Model):
    payment_id = models.CharField(
        'ID de la compra', max_length=200, null=False, blank=False)
    subject = models.CharField(
        'Subject', max_length=500, null=False, blank=False)
    currency = models.CharField(
        'Currency', max_length=20, null=False, blank=False)
    amount = models.CharField(
        'Amount', max_length=100, null=False, blank=False)
    transaction_id = models.CharField(
        'Transaction ID', max_length=200, null=True, blank=True)
    custom = models.CharField(
        'Custom', max_length=500, null=True, blank=True)
    body = models.TextField(
        'Body', null=True, blank=True)
    bank = models.CharField(
        'Bank nombre', max_length=200, null=True, blank=True)
    bank_id = models.CharField(
        'Bank ID', max_length=10, null=True, blank=True)
    payment_url = models.URLField(
        'Payment URL', null=True, blank=True)
    simplified_transfer_url = models.URLField(
        'Simplified URL', null=True, blank=True)
    transfer_url = models.URLField(
        'Transfer URL', null=True, blank=True)
    app_url = models.URLField(
        'App URL', null=True, blank=True)
    return_url = models.URLField(
        'Return URL', null=True, blank=True)
    cancel_url = models.URLField(
        'Cancel URL', null=True, blank=True)
    picture_url = models.URLField('Picture URL', null=True, blank=True)
    notify_url = models.URLField('Notify URL', null=True, blank=True)
    contract_url = models.URLField('Contract URL', null=True, blank=True)
    notify_api_version = models.CharField(
        'API Version notify', max_length=10, null=True, blank=True)
    expires_date = models.DateTimeField('Expires', null=True, blank=True)
    send_email = models.BooleanField('Send email', default=False)
    payer_name = models.CharField(
        'Payer name', max_length=300, null=True, blank=True)
    payer_email = models.CharField(
        'Payer email', max_length=200, null=True, blank=True)
    send_reminders = models.BooleanField('Reminders', default=False)
    responsible_user_email = models.CharField(
        'Responsable del pago', max_length=200, null=True, blank=True)
    personal_identifier = models.CharField(
        'Identificador personal pagador',
        max_length=100,
        null=True,
        blank=True)
    fixed_payer_personal_identifier = models.CharField(
        'Identificador personal', max_length=30, null=True, blank=True)
    integrator_fee = models.CharField(
        'Comision integrador', max_length=100, null=True, blank=True)
    ready_for_terminal = models.BooleanField(
        'Ready for terminal', default=False)
    notification_token = models.CharField(
        'Token verificacion Khipu', max_length=400, null=True, blank=True)
    receiver_id = models.IntegerField(
        'Receiver ID', null=True, blank=True)
    conciliation_date = models.DateTimeField(
        'Concilation date', null=True, blank=True)
    status = models.CharField(
        'Status payment',
        max_length=50,
        choices=PAYMENT_STATUS,
        null=True,
        blank=True)
    status_detail = models.CharField(
        'Status payments detail',
        max_length=50,
        choices=PAYMENT_STATUS_DETAIL,
        null=True,
        blank=True)
    receipt_url = models.URLField(
        'URL comprobante', null=True, blank=True)
    attachment_urls = models.TextField(
        'URL archivos adjuntos al pago', null=True, blank=True)
    bank_account_number = models.CharField(
        'Bank account number', max_length=400, null=True, blank=True)
    out_of_date_conciliation = models.BooleanField(
        'Pago fuera de la expiracion', default=False)
    payment_method = models.CharField(
        'Status payment',
        max_length=50,
        choices=PAYMENT_METHOD,
        null=True,
        blank=True)

    class Meta:
        db_table = 'payment'
        verbose_name = 'Ordenes de compra Khipu'

    def save(self, **kwargs):
        mfields = iter(self._meta.fields)
        mods = [(f.attname, kwargs[f.attname]) for f in mfields if f.attname in kwargs]  # noqa
        for fname, fval in mods:
            setattr(self, fname, fval)
        super(Payment, self).save()

    def send_signals(self):
        """
        Enviar un Signal para la app Django
        """
        if self.status == 'done':  # Pagado
            payment_successful.send(sender=self)
        elif self.status == 'amount_error':
            payment_amount_error.send(sender=self)
        elif self.status == 'receiver_error':
            payment_receiver_id_error.send(sender=self)

    def __unicode__(self):
        return u"Orden de compra Khipu {}".format(self.payment_id)
