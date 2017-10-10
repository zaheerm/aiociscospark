import asyncio
from aiociscospark import webhooks
import os

import pytest

@pytest.mark.asyncio
async def test_create_list_delete():
    access_token = os.environ.get("TOKEN")
    webhooks_api = webhooks.Webhooks(access_token)
    webhook = await webhooks_api.create("test", "http://127.0.0.1", "messages", "created")
    assert webhook.url == "http://127.0.0.1"
    assert webhook.name == "test"
    assert webhook.resource == "messages"
    assert webhook.event == "created"
    all_webhooks = await webhooks_api.list()
    assert len(all_webhooks) >= 1
    _ = await webhook.delete()
