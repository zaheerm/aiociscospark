import json
import requests


WEBHOOK_URL = "https://api.ciscospark.com/v1/webhooks"


def create(name, url, resource, event, access_token):
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


def delete(id, access_token):
    headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(access_token)}
    try:
        print("Deleting spark webhook {}".format(id))
        req = requests.delete(WEBHOOK_URL + "/{}".format(id), headers=headers)
        if req.status_code == 204:
            return True
        else:
            print(req)
    except Exception as exc:
        print(exc)
    return False


def list(access_token):
    headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(access_token)}
    try:
        print("Listing spark webhooks")
        req = requests.get(WEBHOOK_URL, headers=headers)
        if req.status_code == 200:
            return req.json()
        else:
            print(req)
    except Exception as exc:
        print(exc)
    return None


if __name__ == '__main__':
    access_token = open("access_token.txt").read().strip()
    webhook_id = create("test", "http://127.0.0.1", "messages", "created", access_token)
    if webhook_id:
        print("Created webhook with id {}".format(webhook_id))
        if not delete(webhook_id, access_token):
            print("Failed to delete webhook {}".format(webhook_id))
        else:
            webhooks = list(access_token)
            if webhooks:
                for item in webhooks.get("items", []):
                    if not delete(item["id"], access_token):
                        print("Failed to delete webhook {}".format(item["id"]))
    else:
        print("Failed to create webhook")
