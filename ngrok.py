import aiohttp
import asyncio
import json


class NgrokError(Exception):
    pass


async def create_tunnel(name, port, loop=None):
    print("Creating ngrok tunnel {}".format(name))
    data_to_post = json.dumps({"addr": "8080", "proto": "http", "name": name})
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


if __name__ == '__main__':
    async def main(loop):
        url = await create_tunnel("test", 8080, loop=loop)
        if url:
            print("Tunnel created at {}".format(url))
            result = await delete_tunnel("test")
            if not result:
                print("Failed to delete tunnel")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
