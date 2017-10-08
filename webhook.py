import json
import requests


def _headers(access_token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(access_token)}
    return headers


class Webhook:
    def __init__(self, access_token, webhook_url, name, url, resource, event):
        self._access_token = access_token
        self.webhook_url = webhook_url
        self.name = name
        self.url = url
        self.resource = resource
        self.event = event

    def __str__(self):
        return "{} mapping {}:{} to {}".format(self.name, self.resource, self.event, self.url)

    def __repr__(self):
        return "<Webhook {}:{} for {}:{}>".format(self.name, self.url, self.resource, self.event)

    def delete(self):
        try:
            print("Deleting spark webhook {}".format(self.webhook_url))
            req = requests.delete(
                self.webhook_url, headers=_headers(self._access_token))
            if req.status_code == 204:
                return True
            else:
                print(req)
        except Exception as exc:
            print(exc)
        return False


class Webhooks:
    WEBHOOK_URL = "https://api.ciscospark.com/v1/webhooks"

    def __init__(self, access_token):
        self._access_token = access_token

    def create(self, name, url, resource, event):
        data_to_post = json.dumps({
            "name": name,
            "targetUrl": url,
            "resource": resource,
            "event": event})
        headers = _headers(self._access_token)
        try:
            print("Creating spark webhook {} to point to {}".format(name, url))
            req = requests.post(self.WEBHOOK_URL, headers=headers, data=data_to_post).json()
            return Webhook(
                self._access_token,
                self.WEBHOOK_URL + "/{}".format(req["id"]), name, url, resource, event)
        except Exception as exc:
            print(exc)
        return None

    def list(self):
        try:
            webhooks = []
            print("Listing spark webhooks")
            req = requests.get(self.WEBHOOK_URL, headers=_headers(self._access_token))
            if req.status_code == 200:
                for webhook in req.json().get("items", []):
                    webhooks.append(Webhook(
                        self._access_token,
                        "{}/{}".format(self.WEBHOOK_URL, webhook["id"]),
                        webhook["name"],
                        webhook["targetUrl"],
                        webhook["resource"],
                        webhook["event"]
                    ))
                return webhooks
            else:
                print(req)
        except Exception as exc:
            print(exc)
        return None


if __name__ == '__main__':
    access_token = open("access_token.txt").read().strip()
    webhooks = Webhooks(access_token)
    webhook = webhooks.create("test", "http://127.0.0.1", "messages", "created")
    if webhook:
        print("Created webhook {}".format(webhook))
        all_webhooks = webhooks.list()
        print(all_webhooks)
        if all_webhooks:
            for item in all_webhooks:
                if not item.delete():
                    print("Failed to delete webhook {}".format(item))
    else:
        print("Failed to create webhook")
