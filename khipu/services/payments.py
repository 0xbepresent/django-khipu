# -*- coding: utf-8 -*-
from collections import OrderedDict

from .common import KhipuService
from ..exceptions import KhipuError
from ..models import Payment


class CreatePayment(KhipuService):
    """
    Crear pago obtener la URL Khipu para usarse por los pagadores.
    @Parameters
        subject: el asunto del cobro. Con un máximo de 255 caracteres.
        currency: Parámetro de formulario — El código de moneda formato
        ISO-4217
        amount: el monto del cobro.
        transaction_id:
            en esta variable puedes enviar un identificador propio de tu
            transacción, como un número de factura.
        custom:
            en esta variable puedes enviar información personalizada de la
            transacción, como por ejemplo, instrucciones de preparación
            o dirección de envio.
        body: descripción del cobro.
        bank_id:
            el código del banco.
            Puedes obtener los códigos usando la llamada GetBanks
        return_url:
            la dirección URL a donde enviar al cliente cuando el pago está
            siendo verificado
        cancel_url:
            la dirección URL a donde enviar al cliente si se arrepiente
            de hacer la transacción
        picture_url:
            una dirección URL de una foto de tu producto o servicio
            para mostrar en la página del cobro
        notify_url:
            Parámetro de formulario — La dirección del web-service que
            utilizará khipu para notificar cuando el pago esté conciliado
        contract_url:
            Parámetro de formulario — La dirección URL del archivo PDF con el
            contrato a firmar mediante este pago.
            El cobrador debe estar habilitado para este servicio y el campo
            'fixed_payer_personal_identifier' es obgligatorio
        notify_api_version:
            Parámetro de formulario — Versión de la API de notifiaciones para
            recibir avisos por web-service
        expires_date:
            fecha de expiración del cobro. Pasada la fecha el cobro es
            inválido.
            Formato Unix timestamp. Debe corresponder a una fecha en el futuro.
        send_email:
            Parámetro de formulario — Si es 'true', se enviará una solicitud
            de cobro al correo especificado en 'payer_email'
        payer_name:
            Parámetro de formulario — Nombre del pagador.
            Es obligatorio cuando send_email es 'true'
        payer_email:
            Parámetro de formulario — Correo del pagador.
            Es obligatorio cuando send_email es 'true'
        send_reminders:
            Parámetro de formulario — 'true' se enviarán recordatorios de
            cobro.
        responsible_user_email:
            Parámetro de formulario — Correo electrónico del responsable de
            este cobro, debe corresponder a un usuario khipu con permisos para
            cobrar usando esta cuenta de cobro
        fixed_payer_personal_identifier:
            Parámetro de formulario — Identificador personal. Si se especifica,
            solo podrá ser pagado usando ese identificador
        integrator_fee:
            Parámetro de formulario — Comisión para el integrador. Sólo es
            válido si la cuenta de cobro tiene una cuenta de integrador
            asociada
    @Return Values
        payment_id:
            String Identificador único del pago, alfanumérica 12 caracteres
        payment_url:
            String URL principal del pago, si el usuario no ha elegido
            previamente un método de pago se le muestran las opciones
        simplified_transfer_url:
            String URL de pago simplificado
        transfer_url:
            String URL de pago normal
        app_url:
            String URL para invocar el pago desde un dispositivo móvil usando
            la APP de khipu
        ready_for_terminal:
            Boolean Es 'true' si el pago ya cuenta con todos los datos
            necesarios para abrir directamente la aplicación de pagos khipu
    """
    def __init__(self, receiver_id, secret, service_name, **kwargs):
        super(CreatePayment, self).__init__(
            receiver_id, secret, service_name, **kwargs)
        self.method = 'POST'
        self.path = 'payments'
        fields = [
            'amount', 'bank_id', 'body', 'cancel_url', 'contract_url',
            'currency', 'custom', 'expires_date',
            'fixed_payer_personal_identifier', 'integrator_fee',
            'notify_api_version', 'notify_url', 'payer_email', 'payer_name',
            'picture_url', 'responsible_user_email', 'return_url',
            'send_email', 'send_reminders', 'subject', 'transaction_id'
        ]
        if kwargs.get('amount') and kwargs.get('currency')\
                and kwargs.get('subject'):
            self.data = OrderedDict()
            for field in fields:
                if kwargs.get(field):
                    if type(kwargs.get(field)) == bool:
                        self.data[field] = str(kwargs.get(field)).lower()
                    else:
                        self.data[field] = kwargs.get(field)
        else:
            raise KhipuError('Amount, currency and subject are necessary.')

        self.request()  # Llamar al servicio Khipu

        # Con la data respuesta creamos data en el modelo.
        data_to_model = kwargs.copy()
        data_to_model.update(self.data_response)
        Payment.objects.create(**data_to_model)


class GetPayment(KhipuService):
    """
    Obtener la info de un pago mediante un Token que Khipu nos proporciona.
    @Parameters
        notification_token: Token que Khipu nos proporciona en una llamada API.
    @Return Values:
        payment_id:
            String Identificador único del pago, es una cadena alfanumérica de
            12 caracteres
        payment_url:
            String URL principal del pago, si el usuario no ha elegido
            previamente un método de pago se le muestran las opciones
        simplified_transfer_url:
            String URL de pago simplificado
        transfer_url:
            String URL de pago normal
        app_url:
            String URL para invocar el pago desde un dispositivo móvil usando
            la APP de khipu
        ready_for_terminal:
            Boolean Es 'true' si el pago ya cuenta con todos los datos
            necesarios para abrir directamente la aplicación de pagos khipu
        notification_token:
            String Cadena de caracteres alfanuméricos que identifican
            unicamente al pago, es el identificador que el servidor de khipu
            enviará al servidor del comercio cuando notifique que un pago está
            conciliado
        receiver_id:
            Long Identificador único de una cuenta de cobro
        conciliation_date:
            Date Fecha y hora de conciliación del pago. Formato ISO-8601.
            Ej: 2017-03-01T13:00:00Z
        subject:
            String Motivo del pago
        amount:
            Double
        currency:
            String El código de moneda en formato ISO-4217
        status:
            String Estado del pago, puede ser 'pending'
            (el pagador aún no comienza a pagar), 'verifying'
            (se está verificando el pago) o 'done', el pago ya está confirmado
        status_detail:
            String Detalle del estado del pago,
            'pending' (el pagadon aún no comienza a pagar),
            'normal' (el pago fue verificado y cancelado por algún medio de
            pago),
            'marked-paid-by-receiver' (el cobrador marco el cobro como pagado
            por otro medio),
            'rejected-by-payer' (el pagador declaró que no pagará),
            'marked-as-abuse' (el pagador declaró que no pagará y que el
            cobro fue no solicitado)
            'reversed' (el pago fue anulado por el comercio,
            el dinero fue devuelto al pagador).
        body:
            String Detalle del cobro
        picture_url:
            String URL de cobro
        receipt_url:
            String URL del comprobante de pago
        return_url:
            String URL donde se redirige al pagador luego que termina el pago
        cancel_url:
            String URL donde se redirige al pagador luego de que desiste hacer
            el pago
        notify_url:
            String URL del webservice donde se notificará el pago
        notify_api_version:
            String Versión de la api de notificación
        expires_date:
            Date Fecha de expiración del pago. En formato ISO-8601
        attachment_urls:
            array[String] URLs de archivos adjuntos al pago
        bank:
            String Nombre del banco seleccionado por el pagador
        bank_id:
            String Identificador del banco seleccionado por el pagador
        payer_name:
            String Nombre del pagador
        payer_email:
            String Correo electrónico del pagador
        personal_identifier:
            String Identificador personal del pagador
        bank_account_number:
            String Número de cuenta bancaria del pagador
        out_of_date_conciliation:
            Boolean Es 'true' si la conciliación del pago fue hecha luego de la
            fecha de expiración
        transaction_id:
            String Identificador del pago asignado por el cobrador
        custom:
            String Campo genérico que asigna el cobrador al momento de hacer
            el pago
        responsible_user_email:
            String Correo electrónico de la persona responsable del pago
        send_reminders:
            Boolean Es 'true' cuando este es un cobro por correo electrónico
            y khipu enviará recordatorios
        send_email:
            Boolean Es 'true' cuando khipu enviará el cobro por correo
            electrónico
        payment_method:
            String Método de pago usado por el pagador, puede ser
            'regular_transfer' (transferencia normal),
            'simplified_transfer' (transferencia simplificada) o
            'not_available' (para un pago marcado como realizado por otro medio
            por el cobrador).
    """

    def __init__(self, receiver_id, secret, service_name, **kwargs):
        super(GetPayment, self).__init__(
            receiver_id, secret, service_name, **kwargs)
        self.method = 'GET'
        self.path = 'payments'
        notification_token = kwargs.get('notification_token')
        if notification_token:
            self.data = {"notification_token": notification_token}
        else:
            raise KhipuError('notification_token field is necessary.')

        self.request()  # Llamar al servicio Khipu
