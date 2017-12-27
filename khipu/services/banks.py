from .common import KhipuService


class GetBanks(KhipuService):
    """
    Servicio que ayudara a obtener todos los bancos disponible en Khipu.
    """

    def __init__(self, receiver_id, secret, service_name, **kwargs):
        super(GetBanks, self).__init__(
            receiver_id, secret, service_name, **kwargs)
        self.method = 'GET'
        self.path = 'banks'

        self.request()  # Llamar al servicio Khipu
