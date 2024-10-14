from aiohttp import ClientError
from fastapi import HTTPException

from modules.base_adapter import BaseAioAdapter

class ExchangeAioAdapter(BaseAioAdapter):
    def __init__(self, route_manager, api_key):
        super().__init__(route_manager)
        self.api_key = api_key

    async def retrieve_exchange(self, base_currency: str, target_currency: str):
        try:
            params = {'apikey': self.api_key, 'base_currency': base_currency, 'currencies': target_currency}
            exchange_data = await self._get('get_exchange_rate', params=params)
            if 'data' not in exchange_data or target_currency not in exchange_data['data']:
                raise HTTPException(status_code=400, detail="Invalid currency pair")

            return exchange_data
        except ClientError as e:
            raise HTTPException(status_code=503, detail="Currency API is unavailable")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal server error")