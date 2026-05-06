from __future__ import annotations

import httpx
from urllib.parse import urlparse


class APIVoidError(Exception):
    pass


class APIVoidClient:
    BASE_URL = "https://endpoint.apivoid.com/domainbl/v1/pay-as-you-go/"

    def __init__(self, api_key: str, timeout: float = 5.0):
        self.api_key = api_key
        self.timeout = timeout

    def extract_domain(self, url: str) -> str:
        return urlparse(url).netloc

    async def check_domain(self, url: str) -> dict:
        domain = self.extract_domain(url)

        params = {
            "key": self.api_key,
            "host": domain
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(self.BASE_URL, params=params)

            response.raise_for_status()
            payload = response.json()

            if "data" not in payload:
                raise APIVoidError("Malformed APIVoid response")

            return payload["data"]

        except Exception as e:
            raise APIVoidError(str(e))