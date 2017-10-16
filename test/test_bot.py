import asyncio
from aiociscospark import bot
from aiociscospark import messages, people
import os
from unittest import mock
import pytest


class AsyncMock(mock.MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)


class BotForTests(bot.CommandBot):
    @bot.botcommand
    async def hmm(self, options):
        """
        test summary
        Usage: hmm
        """
        return "test result"

    def voodoo(self):
        pass

    @bot.botcommand
    async def one_arg(self, options):
        """
        test summary
        Usage: one_arg <arg>
        """
        return "test result"

    @bot.botcommand
    async def broken(self, options):
        """
        test summary
        Usage: broken
        """
        raise Exception("broken")


@pytest.mark.asyncio
async def test_command_bot_with_commands(event_loop):
    access_token = os.environ.get("TOKEN")
    bot = BotForTests(access_token, "https://127.0.0.1", event_loop)
    assert await bot.run_command("notacommand") == "I don't recognise that command"
    assert await bot.run_command("voodoo") == "I don't recognise that command"
    assert await bot.run_command("hmm") == "test result"
    assert await bot.run_command("one_arg arg") == "test result"
    result = await bot.run_command("one_arg")
    assert "Command given not matching usage." in result
    assert await bot.run_command("broken") == "That didn't work as expected"
    result = await bot.run_command("help")
    assert "test summary" in result
    result = await bot.run_command("help hmm")
    assert bot.hmm.__doc__ in result
    assert await bot.run_command("help voodoo") == "There is no command named voodoo"
    assert await bot.run_command("help notacommand") == "There is no command named notacommand"


@pytest.mark.asyncio
async def test_message_sent_by_me(event_loop):
    access_token = os.environ.get("TOKEN")
    bot = BotForTests(access_token, "https://127.0.0.1", event_loop)
    request = AsyncMock()
    request.json.return_value = {"data": {"roomId": "blah", "id": "foo", "personId": "person1"}}
    with mock.patch.object(bot, "people", new_callable=AsyncMock) as people_mock:
        with mock.patch.object(bot, "messages", new_callable=AsyncMock) as messages_mock:
            people_mock.me.return_value.person_id = "person1"
            await bot.message_created(request)
            assert not messages_mock.send_to_person.called
            assert not messages_mock.send_to_room.called


@pytest.mark.asyncio
async def test_message_sent_directly(event_loop):
    access_token = os.environ.get("TOKEN")
    bot = BotForTests(access_token, "https://127.0.0.1", event_loop)
    request = AsyncMock()
    request.json.return_value = {"data": {"roomId": "blah", "id": "foo", "personId": "person1"}}
    with mock.patch.object(bot, "people", new_callable=AsyncMock) as people_mock:
        with mock.patch.object(bot, "messages", new_callable=AsyncMock) as messages_mock:
            people_mock.me.return_value.person_id = "person2"
            messages_mock.get.return_value = messages.Message(
                access_token, None, "foo", "text", "blah", "direct", "person1", "person1email",
                None)
            await bot.message_created(request)
            assert messages_mock.send_to_person.called
            assert not messages_mock.send_to_room.called


@pytest.mark.asyncio
async def test_message_sent_to_room(event_loop):
    access_token = os.environ.get("TOKEN")
    bot = BotForTests(access_token, "https://127.0.0.1", event_loop)
    request = AsyncMock()
    request.json.return_value = {"data": {"roomId": "blah", "id": "foo", "personId": "person1"}}
    with mock.patch.object(bot, "people", new_callable=AsyncMock) as people_mock:
        with mock.patch.object(bot, "messages", new_callable=AsyncMock) as messages_mock:
            people_mock.me.return_value.person_id = "person2"
            messages_mock.get.return_value = messages.Message(
                access_token, None, "foo", "text", "blah", "room", "person1", "person1email",
                None)
            people_mock.get.return_value = people.Person(access_token, None, "person1", "boo")
            await bot.message_created(request)
            assert not messages_mock.send_to_person.called
            assert messages_mock.send_to_room.called
