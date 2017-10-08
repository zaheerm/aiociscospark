from aiohttp import web
import requests
import json
import ngrok


WEBHOOK_URL = "https://api.ciscospark.com/v1/webhooks"


def create_webhook(name, url, resource, event, access_token):
    data_to_post = json.dumps({"name": name, "targetUrl": url, "resource": resource, "event": event})
    headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(access_token)}
    try:
        print("Creating spark webhook {} to point to {}".format(name, url))
        req = requests.post(WEBHOOK_URL, headers=headers, data=data_to_post).json()
        print(req)
        return req["id"]
    except Exception as exc:
        print(exc)
    return None


def delete_webhook(id, access_token):
    headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(access_token)}
    try:
        print("Deleting spark webhook {}".format(id))
        req = requests.delete(WEBHOOK_URL + "/{}".format(id))
        if req.status_code == 204:
            return True
    except Exception as exc:
        print(exc)
    return None


async def handle(request):
    data = await request.json()
    print("Got data {}".format(data))
    room_id = data["data"]["roomId"]
    message_id = data["data"]["id"]
    person_id = data["data"]["personId"]

    return web.Response(text=str(data))


def main(public_url):
    print(public_url)
    app = web.Application()
    app.router.add_post('/', handle)
    app.router.add_post('/{name}', handle)
    web.run_app(app)


if __name__ == '__main__':
    access_token = open("access_token.txt").read().strip()
    port = 8080
    url = ngrok.create_tunnel("sysdig_bot", 8080)
    webhook_id = create_webhook("incoming", url, "messages", "created", access_token)
    main(url)
    delete_webhook(webhook_id, access_token)
    ngrok.delete_tunnel("sysdig_bot")
