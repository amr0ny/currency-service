from modules.exchange.exchange_adapter import ExchangeAioAdapter

from decimal import Decimal
from schemas.exchange import ExchangeRequest, ExchangeResponse
from modules.exchange.exchange_adapter import ExchangeAioAdapter


class ExchangeService:
    def __init__(self, module: ExchangeAioAdapter):
        self.exchange_adapter = module

    async def get_exchange(self, request: ExchangeRequest) -> ExchangeResponse:
        async with self.exchange_adapter as adapter:
            exchange_data = await adapter.retrieve_exchange(request.from_currency, request.to_currency)
            rate = Decimal(str(exchange_data['data'][request.to_currency]['value']))

            amount_as_decimal = Decimal(str(request.value))
            print(amount_as_decimal * rate)
            converted_amount = amount_as_decimal * rate

            return ExchangeResponse(
                from_currency=request.from_currency,
                to_currency=request.to_currency,
                exchange_rate=rate,
                amount=amount_as_decimal,
                converted_amount=converted_amount.quantize(Decimal('0.01')))