import asyncio
from aiociscospark import people, messages, common
import os

import pytest


@pytest.mark.asyncio
async def test_create_get_and_delete_message():
    access_token1 = os.environ.get("TOKEN")
    access_token2 = os.environ.get("TOKEN2")
    people_api1 = people.People(access_token1)
    people_api2 = people.People(access_token2)

    me1 = await people_api1.me()
    me2 = await people_api2.me()

    messages_api = messages.Messages(access_token1)
    sent_message = await messages_api.send_to_person(person_id=me2.person_id, message_text="boo")
    got_message = await messages_api.get(sent_message.message_id)
    assert sent_message == got_message
    result = await got_message.delete()
    with pytest.raises(common.CiscoSparkAPIError):
        got_message = await messages_api.get(sent_message.message_id)


@pytest.mark.asyncio
async def test_create_message_failures():
    access_token = os.environ.get("TOKEN")
    people_api = people.People(access_token)

    me = await people_api.me()

    messages_api = messages.Messages(access_token)
    with pytest.raises(common.CiscoSparkAPIError):
        _ = await messages_api.send_to_person(message_text="boo")
    with pytest.raises(common.CiscoSparkAPIError):
        _ = await messages_api.send_to_person(person_id=me.person_id)
    with pytest.raises(common.CiscoSparkAPIError):
        _ = await messages_api.send_to_person(message_markdown="boo")
    with pytest.raises(common.CiscoSparkAPIError):
        _ = await messages_api.send_to_person(person_email=me.person_id)
