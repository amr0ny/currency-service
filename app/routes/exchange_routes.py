

from fastapi import APIRouter, Depends, Query, HTTPException
from dependency_injector.wiring import inject, Provide

from containers import Services
from schemas.exchange import ExchangeRequest
from services.exchange_service import ExchangeService

exchange_router = APIRouter()
@exchange_router.get("/rates/")
@inject
async def get_rate(
    from_currency: str = Query(..., alias='from'),  # используем alias для 'from'
    to_currency: str = Query(..., alias='to'),      # используем alias для 'to'
    value: float = Query(..., gt=0),                # добавляем ограничение на значение
    exchange_service: ExchangeService = Depends(Provide[Services.exchange_service])
):
    request = ExchangeRequest(
        from_currency=from_currency,
        to_currency=to_currency,
        value=value
    )
    try:
        exchange_response = await exchange_service.get_exchange(request)
        return {
            'result': exchange_response.converted_amount
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))