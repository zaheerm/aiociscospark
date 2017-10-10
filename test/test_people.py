import asyncio
from aiociscospark import people
import os

import pytest


@pytest.mark.asyncio
async def test_create_get_me():
    access_token = os.environ.get("TOKEN")
    people_api = people.People(access_token)
    me = await people_api.me()
    me_by_id = await people_api.get(me.person_id)
    assert me == me_by_id
