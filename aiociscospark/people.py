import aiohttp
import asyncio
import json
from .common import CiscoSparkAPIError
from .common import headers as _headers
from .common import CiscoSparkObject


class Person(CiscoSparkObject):
    def __init__(self, access_token, person_url, person_id, display_name, loop=None):
        super().__init__(access_token, loop=loop)
        self.person_url = person_url
        self.person_id = person_id
        self.display_name = display_name

    def __str__(self):
        return self.display_name

    def __repr__(self):
        return "<Person {}:{}>".format(self.person_id, self.display_name)

    def __eq__(self, other):
        return (
            self.person_id == other.person_id and
            self.person_url == other.person_url and
            self.display_name == other.display_name)

    async def delete(self):
        async with aiohttp.ClientSession(
                loop=self._loop,
                headers=_headers(self._access_token)) as client:
            async with client.delete(self.person_url) as resp:
                return resp.status == 204


class People(CiscoSparkObject):
    PEOPLE_URL = "https://api.ciscospark.com/v1/people"

    def _person_from_result(self, result):
        return Person(
            self._access_token,
            "{}/{}".format(self.PEOPLE_URL, result["id"]),
            result["id"],
            result["displayName"],
            loop=self._loop
            )

    async def get(self, person_id):
        async with aiohttp.ClientSession(
                loop=self._loop,
                headers=_headers(self._access_token)) as client:
            async with client.get(url="{}/{}".format(self.PEOPLE_URL, person_id)) as resp:
                result = await resp.json()
                if resp.status == 200:
                    return self._person_from_result(result)
                else:
                    raise CiscoSparkAPIError(result)

    async def me(self):
        async with aiohttp.ClientSession(
                loop=self._loop,
                headers=_headers(self._access_token)) as client:
            async with client.get(url="{}/me".format(self.PEOPLE_URL)) as resp:
                result = await resp.json()
                if resp.status == 200:
                    return self._person_from_result(result)
                else:
                    raise CiscoSparkAPIError(result)
