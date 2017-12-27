Django-Khipu
==================

Aplicacion de integracion entre Django y [Pagos Khipu](https://khipu.com/).
[![Travis CI](https://travis-ci.org/misalabs/django-khipu.svg?branch=master)](https://travis-ci.org/felicesyforrados/django-webpay)
[![Coverage Status](https://coveralls.io/repos/github/felicesyforrados/django-webpay/badge.svg?branch=master)](https://coveralls.io/github/felicesyforrados/django-webpay?branch=master)


Configuración
==============

 * Variables en settings.py de tu proyecto Django.
     * Indentificador único de la cuenta de cobro:
  KHIPU_RECEIVER_ID = '236987'
  
     * Llave secreta y única de la cuenta de cobro:
  KHIPU_SECRET_KEY = '9kmbf4fckm81f9892a291a12d0m10cdf389'

 * Poner khipu en tus INSTALLED_APPS.

 * Crear las migraciones necesarias para obtener la tabla de datos de Khipu en tu proyecto.
```
$ python manage.py migrate khipu
```

 * Referenciar en tu proyecto las URLs de Khipu:
```
urlpatterns = [
    url(r'^khipu/', include('khipu.urls')),
]
```

Uso mediante API
================

Usar el servicio para crear las URLs de pago y obtener el JSON de URL's Khipu
y usarlas donde quieras.
```
>> from khipu.api import Khipu
>> khipu = Khipu()
>> result = khipu.service('CreatePayment', **{
    'subject': 'Esto es un pago de pruebas',
    'currency': 'CLP',
    'amount': '3000.0000'
   })
>> {u'payment_id': u'weyayhnbmker', u'app_url': u'khipu:///pos/weyayhnbmker', u'ready_for_terminal': False, u'payment_url': u'https://khipu.com/payment/info/weyayhnbmker', u'simplified_transfer_url': u'https://app.khipu.com/payment/simplified/weyayhnbmker', u'transfer_url': u'https://khipu.com/payment/manual/weyayhnbmker'}
```

Uso mediante Django-Forms
================

Usar el formulario pre-armado para crear botones facilmente.
```
>> from khipu.forms import KhipuCreatePaymentForm
>> form_payment_khipu = KhipuCreatePaymentForm(**{
        'subject': 'Esto es un pago de pruebas via Django-Form',
        'currency': 'CLP',
        'amount': '6000.0000'
    })
    return render(request, 'carro.html', {'form_payment_khipu': form_payment_khipu})
```
Y en el Template Django hacer:
```
{{form_payment_khipu.render}}
```

Servicios
=========
Descripción de los servicios que pueden usarse para interactuar con Khipu.

 * GetBanks: Obtener los bancos disponibles que el pagador puede usar.
 * 'CreatePayment'. Crear la orden de pago en Khipu y que nos devuelvan las URLs.
     * Se pueden enviar los siguientes parametros:
        * subject (obligatorio)
        * currency (obligatorio)
        * amount (obligatorio)
        * transaction_id
        * custom
        * body
        * bank_id
        * return_url
        * cancel_url
        * picture_url
        * notify_url
        * contract_url
        * notify_api_version
        * expires_date
        * send_email
        * payer_name
        * send_reminders
        * responsible_user_email
        * fixed_payer_personal_identifier
        * integrator_fee
     * Se reciben los siguientes parametros por parte de Khipu:
         * payment_id
         * payment_url
         * simplified_transfer_url
         * transfer_url
         * app_url
         * ready_for_terminal

Signals
======

Signals los cuales el Proyecto Django puede recibir para saber ciertas cosas:

 - payment_successful: Cuando el pago es "done" y hay que entregarle el bien o servicio al pagador.
 - payment_amount_error: Existe un error con el monto que dijimos que pagara y el monto que nos llego. Hay que revisar ya que muy probablemente tiene que reembolsarse el dinero.
 - payment_receiver_id_error: Existe un error con el receiver_id pues no es el mismo que nosotros usamos. Es un error muy raro y  hay que revisar ya que muy probablemente tiene que reembolsarse el dinero.

Tests
=====

Para ejecutar los tests hay que tener instalado django, requests y mock.
```
$ python run_tests.py
```

Contacto
========
hi@misalabs.com