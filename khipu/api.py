# -*- coding: utf-8 -*-
import logging

from django.conf import settings

from . import services
from .exceptions import KhipuError

logger = logging.getLogger(__name__)


class Khipu(object):
    """
    Método formal para la comunicacion con Khipu
    """

    def __init__(self):
        self.services = [
            'GetBanks',
            'CreatePayment',
            'GetPayment',
        ]

    def service(self, service_name, **kwargs):
        """
        Llamar los servicios disponibles de Khipu.
        @Parametros:
            service_name: Nombre del servicio requerido de Khipu.
            kwargs: Dict con data que necesita el servicio.
        @Return
            Objeto Request que responde Khipu.
        """
        if service_name in self.services:
            if settings.KHIPU_RECEIVER_ID and settings.KHIPU_SECRET_KEY:
                service = getattr(
                    services, service_name
                )(
                    settings.KHIPU_RECEIVER_ID, settings.KHIPU_SECRET_KEY,
                    service_name, **kwargs)
                return service.response()
            else:
                msg = """
                    Necessary authentication for the service {} {} {}
                    """.format(
                    service_name,
                    settings.KHIPU_SECRET_KEY,
                    settings.KHIPU_RECEIVER_ID)
                logger.error(msg)
                raise KhipuError(msg)
        else:
            msg = "Service does not exist {}".format(service_name)
            logger.error(msg)
            raise KhipuError(msg)
