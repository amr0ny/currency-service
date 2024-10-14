from dependency_injector import containers, providers

from modules.base_adapter import BaseAioAdapter
from modules.exchange.exchange_adapter import ExchangeAioAdapter
from modules.exchange.route_manager import ExchangeRouteManager
from services.exchange_service import ExchangeService
from settings import settings


class Adapters(containers.DeclarativeContainer):
    config = providers.Configuration()

    exchange_adapter = providers.Singleton(ExchangeAioAdapter,
                                           route_manager=ExchangeRouteManager(),
                                           api_key=settings.SERVICE_API_KEY)


class Services(containers.DeclarativeContainer):
    config = providers.Configuration()

    exchange_service = providers.Singleton(ExchangeService,
                                           module=Adapters.exchange_adapter)
