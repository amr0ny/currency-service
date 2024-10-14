from modules.base_adapter import BaseRouteManager

class ExchangeRouteManager(BaseRouteManager):
    def __init__(self):
        base_url = 'https://api.currencyapi.com/v3'
        routes = {
            'get_exchange_rate': '/latest'
        }
        super().__init__(base_url, routes)
