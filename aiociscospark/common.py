import asyncio


class CiscoSparkAPIError(Exception):
    pass


class CiscoSparkObject:
    def __init__(self, access_token, loop=None):
        self._access_token = access_token
        if loop:
            self._loop = loop
        else:
            self._loop = asyncio.get_event_loop()


def headers(access_token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(access_token)}
    return headers
