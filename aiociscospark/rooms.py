import aiohttp
import asyncio
import json
from .common import CiscoSparkAPIError
from .common import headers as _headers
from .common import CiscoSparkObject


class Room(CiscoSparkObject):
    def __init__(self, access_token, room_url, title, room_type, is_locked, team_id=None,
                 loop=None):
        super().__init__(access_token, loop=loop)
        self.room_url = room_url
        self.title = title
        self.room_type = room_type
        self.is_locked = is_locked
        self.team_id = team_id

    def __str__(self):
        result = "{} room: {}".format(self.room_type, self.title)
        if self.team_id:
            result += " part of team {}".format(self.team_id)
        return result

    def __repr__(self):
        return "<Room {} {}>".format(self.room_type, self.title)

    async def delete(self):
        async with aiohttp.ClientSession(
                loop=self._loop,
                headers=_headers(self._access_token)) as client:
            async with client.delete(self.room_url) as resp:
                return resp.status == 204

    async def update(self):
        data_to_post = json.dumps({"title": self.title})
        async with aiohttp.ClientSession(
                loop=self._loop,
                headers=_headers(self._access_token)) as client:
            async with client.put(self.room_url, data=data_to_post) as resp:
                return resp.status == 200


class Rooms(CiscoSparkObject):
    ROOM_URL = "https://api.ciscospark.com/v1/rooms"

    async def create(self, title, team_id=None):
        data_to_post = {"title": title}
        if team_id:
            data_to_post["teamId"] = team_id
        data_to_post = json.dumps(data_to_post)
        async with aiohttp.ClientSession(
                loop=self._loop,
                headers=_headers(self._access_token)) as client:
            async with client.post(url=self.ROOM_URL, data=data_to_post) as resp:
                result = await resp.json()
                if resp.status == 200:
                    return Room(
                        self._access_token,
                        "{}/{}".format(self.ROOM_URL, result["id"]),
                        result["title"],
                        result["type"],
                        result["isLocked"],
                        result.get("teamId", team_id),
                        loop=self._loop)
                else:
                    raise CiscoSparkAPIError(result)

    async def list(self):
        rooms = []
        async with aiohttp.ClientSession(
                loop=self._loop,
                headers=_headers(self._access_token)) as client:
            async with client.get(url=self.ROOM_URL) as resp:
                result = await resp.json()
                if resp.status == 200:
                    for item in result.get("items", []):
                        rooms.append(Room(
                            self._access_token,
                            "{}/{}".format(self.ROOM_URL, item["id"]),
                            item["title"],
                            item["type"],
                            item["isLocked"],
                            item.get("teamId"),
                            loop=self._loop
                        ))
                    return rooms
                else:
                    raise CiscoSparkAPIError(result)
