import aiohttp
import asyncio
import json
from .common import CiscoSparkAPIError
from .common import headers as _headers
from .common import CiscoSparkObject


class Webhook(CiscoSparkObject):
    def __init__(self, access_token, webhook_url, name, url, resource, event, loop=None):
        super().__init__(access_token, loop=loop)
        self.webhook_url = webhook_url
        self.name = name
        self.url = url
        self.resource = resource
        self.event = event

    def __str__(self):
        return "{} mapping {}:{} to {}".format(self.name, self.resource, self.event, self.url)

    def __repr__(self):
        return "<Webhook {}:{} for {}:{}>".format(self.name, self.url, self.resource, self.event)

    async def delete(self):
        print("Deleting spark webhook {}".format(self.webhook_url))
        async with aiohttp.ClientSession(
                loop=self._loop,
                headers=_headers(self._access_token)) as client:
            async with client.delete(self.webhook_url) as resp:
                return resp.status == 204


class Webhooks(CiscoSparkObject):
    WEBHOOK_URL = "https://api.ciscospark.com/v1/webhooks"

    async def create(self, name, url, resource, event):
        data_to_post = json.dumps({
            "name": name,
            "targetUrl": url,
            "resource": resource,
            "event": event})
        async with aiohttp.ClientSession(
                loop=self._loop,
                headers=_headers(self._access_token)) as client:
            print("Creating spark webhook {} to point to {}".format(name, url))
            async with client.post(url=self.WEBHOOK_URL, data=data_to_post) as resp:
                result = await resp.json()
                if resp.status == 200:
                    return Webhook(
                        self._access_token,
                        self.WEBHOOK_URL + "/{}".format(result["id"]),
                        name,
                        url,
                        resource,
                        event,
                        loop=self._loop)
                else:
                    raise CiscoSparkAPIError(result)

    async def list(self):
        webhooks = []
        async with aiohttp.ClientSession(
                loop=self._loop,
                headers=_headers(self._access_token)) as client:
            print("Listing spark webhooks")
            async with client.get(url=self.WEBHOOK_URL) as resp:
                result = await resp.json()
                if resp.status == 200:
                    for webhook in result.get("items", []):
                        webhooks.append(Webhook(
                            self._access_token,
                            "{}/{}".format(self.WEBHOOK_URL, webhook["id"]),
                            webhook["name"],
                            webhook["targetUrl"],
                            webhook["resource"],
                            webhook["event"],
                            loop=self._loop
                        ))
                    return webhooks
                else:
                    raise CiscoSparkAPIError(result)
