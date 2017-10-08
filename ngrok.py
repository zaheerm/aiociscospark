import requests
import json


def create_tunnel(name, port):
    print("Creating ngrok tunnel {}".format(name))
    data_to_post = json.dumps({"addr": "8080", "proto": "http", "name": name})
    try:
        req = requests.post(
            "http://127.0.0.1:4040/api/tunnels",
            data=data_to_post,
            verify=False,
            headers={"Content-Type": "application/json"}).json()
        return req["public_url"]
    except Exception as exc:
        print(exc)
        return None

def delete_tunnel(name):
    print("Deleting ngrok tunnel {}".format(name))
    try:
        req = requests.delete("http://127.0.0.1:4040/api/tunnels/{}".format(name))
        if req.status_code == 204:
            return True
        else:
            print("Got code: {}".format(req.status_code))
    except Exception as exc:
        print(exc)
    return False


if __name__ == '__main__':
    url = create_tunnel("test", 8080)
    if url:
        print("Tunnel created at {}".format(url))
        result = delete_tunnel("test")
        if not result:
            print("Failed to delete tunnel")
    else:
        print("Failed to create tunnel")
