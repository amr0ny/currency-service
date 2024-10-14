from aiohttp import ClientSession
import asyncio

class Route:
    def __init__(self, template):
        self.template = template

    def build(self, **params):
        return self.template.format(**params)


class BaseRouteManager:
    routes: dict[str, Route]

    def __init__(self, base_url, routes):
        self.base_url = base_url
        self.routes = routes

    def get_route(self, route_name, **params):
        route_template = self.routes.get(route_name)
        if not route_template:
            raise ValueError(f"Route '{route_name}' not found.")

        try:
            route = route_template.format(**params)
        except KeyError as e:
            raise ValueError(f"Missing parameter for route '{route_name}': {e}")

        return f"{self.base_url}{route}"

class BaseAioAdapter:
    def __init__(self, route_manager: BaseRouteManager):
        self.route_manager = route_manager

    async def __aenter__(self):
        self.session = ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _get(self, route_name, params=None):
        try:
            url = self.route_manager.get_route(route_name, params=params)
            async with self.session.get(url, params=params) as response:
                return await response.json()
        except Exception as e:
            print(str(e))

    async def _post(self, route_name, params=None, json_data=None):
        url = self.route_manager.get_route(route_name, params=params)
        async with self.session.post(url, json=json_data) as response:
            return await response.json()

    async def _put(self, route_name, params=None, json_data=None):
        url = self.route_manager.get_route(route_name, params=params)
        async with self.session.put(url, json=json_data) as response:
            return await response.json()

    async def _delete(self, route_name, params=None):
        url = self.route_manager.get_route(route_name, params=params)
        async with self.session.delete(url) as response:
            return await response.json()