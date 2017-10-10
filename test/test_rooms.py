import asyncio
from aiociscospark import rooms
import os

import pytest


@pytest.mark.asyncio
async def test_create_list_delete():
    access_token = os.environ.get("TOKEN")
    rooms_api = rooms.Rooms(access_token)
    room = await rooms_api.create("test")
    assert room.title == "test"
    all_rooms = await rooms_api.list()
    assert len(all_rooms) >= 1
    assert len([room for room in all_rooms if room.title == "test"]) >= 1
    _ = await room.delete()
