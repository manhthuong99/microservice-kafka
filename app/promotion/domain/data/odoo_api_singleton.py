from core.modules.restful_module.odoo_api import OdooApi


class Odoo2ApiSingleton(OdooApi):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.api_base_url = None
        self.access_token = None

    async def init(self, base_url, access_token):
        self.api_base_url = base_url
        self.access_token = access_token
