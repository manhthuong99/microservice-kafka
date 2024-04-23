from core.modules.restful_module.magento2_api import Magento2Api


class Magento2ApiSingleton(Magento2Api):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.api_base_url = None
        self.api_authentication_key = None
        self.api_version = None
        self.store = None

    async def init(self, base_url, bearer_token, api_version, store=None):
        self.api_base_url = base_url
        self.api_authentication_key = bearer_token
        self.api_version = api_version
        self.store = store if store is not None else "default"
