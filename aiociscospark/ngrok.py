import aiohttp
import asyncio
import json


class NgrokError(Exception):
    pass


async def create_tunnel(name, port, loop=None):
    print("Creating ngrok tunnel {}".format(name))
    data_to_post = json.dumps({"addr": str(port), "proto": "http", "name": name})
    if not loop:
        loop = asyncio.get_event_loop()
    async with aiohttp.ClientSession(
            loop=loop,
            headers={"Content-Type": "application/json"}) as client:
        async with client.post(
                url="http://127.0.0.1:4040/api/tunnels",
                data=data_to_post) as resp:
            result = await resp.json()
            if resp.status == 201:
                return result["public_url"]
            else:
                raise NgrokError(result)


async def delete_tunnel(name, loop=None):
    print("Deleting ngrok tunnel {}".format(name))
    if not loop:
        loop = asyncio.get_event_loop()
    async with aiohttp.ClientSession(
            loop=loop,
            headers={"Content-Type": "application/json"}) as client:
        async with client.delete("http://127.0.0.1:4040/api/tunnels/{}".format(name)) as resp:
            return resp.status == 204
