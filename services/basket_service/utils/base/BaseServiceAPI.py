from fastapi import HTTPException

from httpx import AsyncClient


class BaseServiceAPI:

    def __init__(self, base_url: str):
        self.base_api = base_url
        self.session: AsyncClient | None

    async def init_session(self):
        if self.session is None:
            self.session = AsyncClient(timeout=10000)

    async def close(self):
        if self.session:
            await self.session.aclose()
            self.session = None

    async def get(self, url: str, params: dict = None, with_base_url: bool = None):
        api_url = f"{self.base_api}{url}" if with_base_url else url

        async with self.session.get(api_url, params=params) as response:

            if response.status != 200:
                raise HTTPException(response.status, await response.text())

            data = await response.json()
            await self.close()

            return data
