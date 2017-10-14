import aiohttp
import asyncio
import json
from .common import CiscoSparkAPIError
from .common import headers as _headers
from .common import CiscoSparkObject


class Message(CiscoSparkObject):
    def __init__(self, access_token, message_url, message_id, text, room_id, room_type, person_id,
                 person_email, time_created, markdown_text=None, loop=None):
        super().__init__(access_token, loop=loop)
        self.message_url = message_url
        self.message_id = message_id
        self.text = text
        self.room_id = room_id
        self.room_type = room_type
        self.person_id = person_id
        self.person_email = person_email
        self.time_created = time_created
        self.markdown_text = markdown_text

    def __str__(self):
        result = "{} {} sent message: {}".format(self.time_created, self.person_email, self.text)
        return result

    def __repr__(self):
        return "<Message {} from:{} at:{}>".format(self.text, self.person_email, self.time_created)

    def __eq__(self, other):
        return (
            self.message_id == other.message_id and
            self.message_url == other.message_url and
            self.text == other.text and
            self.room_id == other.room_id and
            self.room_type == other.room_type and
            self.person_id == other.person_id and
            self.person_email == other.person_email and
            self.markdown_text == other.markdown_text)

    async def delete(self):
        async with aiohttp.ClientSession(
                loop=self._loop,
                headers=_headers(self._access_token)) as client:
            async with client.delete(self.message_url) as resp:
                return resp.status == 204


class Messages(CiscoSparkObject):
    MESSAGE_URL = "https://api.ciscospark.com/v1/messages"

    def _message_from_result(self, result):
        return Message(
            self._access_token,
            "{}/{}".format(self.MESSAGE_URL, result["id"]),
            result["id"],
            result["text"],
            result["roomId"],
            result["roomType"],
            result["personId"],
            result["personEmail"],
            result["created"],
            markdown_text=result.get("markdown"),
            loop=self._loop
            )

    async def get(self, message_id):
        async with aiohttp.ClientSession(
                loop=self._loop,
                headers=_headers(self._access_token)) as client:
            async with client.get(url="{}/{}".format(self.MESSAGE_URL, message_id)) as resp:
                result = await resp.json()
                if resp.status == 200:
                    return self._message_from_result(result)
                else:
                    raise CiscoSparkAPIError(result)

    async def send_to_person(self, person_id=None, person_email=None, message_text=None,
                             message_markdown=None):
        if not person_id and not person_email:
            raise CiscoSparkAPIError("Sending a message to a person without either id or email")
        if not message_text and not message_markdown:
            raise CiscoSparkAPIError("Sending a message requires text or markdown")
        data_to_post = {}
        if person_id:
            data_to_post["toPersonId"] = person_id
        if person_email:
            data_to_post["toPersonEmail"] = person_email
        if message_text:
            data_to_post["text"] = message_text
        if message_markdown:
            data_to_post["markdown"] = message_markdown
        data_to_post = json.dumps(data_to_post)
        async with aiohttp.ClientSession(
                loop=self._loop,
                headers=_headers(self._access_token)) as client:
            async with client.post(url=self.MESSAGE_URL, data=data_to_post) as resp:
                result = await resp.json()
                if resp.status == 200:
                    return self._message_from_result(result)
                else:
                    raise CiscoSparkAPIError(result)

    async def send_to_room(self, room_id, message_text=None, message_markdown=None):
        if not message_text and not message_markdown:
            raise CiscoSparkAPIError("Sending a message requires text or markdown")
        data_to_post = {}
        data_to_post["roomId"] = room_id
        if message_text:
            data_to_post["text"] = message_text
        if message_markdown:
            data_to_post["markdown"] = message_markdown
        data_to_post = json.dumps(data_to_post)
        async with aiohttp.ClientSession(
                loop=self._loop,
                headers=_headers(self._access_token)) as client:
            async with client.post(url=self.MESSAGE_URL, data=data_to_post) as resp:
                result = await resp.json()
                if resp.status == 200:
                    return self._message_from_result(result)
                else:
                    raise CiscoSparkAPIError(result)
