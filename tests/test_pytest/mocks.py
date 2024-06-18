import httpx
import requests

from multi_api_mocker.definitions import MockAPIResponse


class Fork(MockAPIResponse):
    url = "https://example.com/api/fork"
    method = "POST"
    default_status_code = 200
    default_json = {
        "id": "fork101",
        "message": "Forked project",
        "author": "dev@example.com",
    }


class Commit(MockAPIResponse):
    url = "https://example.com/api/commit"
    method = "GET"
    default_status_code = 200
    default_json = {
        "id": "commit102",
        "message": "Initial commit with project structure",
        "author": "dev@example.com",
        "timestamp": "2023-11-08T12:34:56Z",
    }


class Push(MockAPIResponse):
    url = "https://example.com/api/push"
    method = "POST"
    default_status_code = 200
    default_json = {
        "id": "push102",
        "message": "Pushed commit102",
        "author": "dev@example.com",
        "timestamp": "2023-11-08T12:34:56Z",
    }


class PushTimeoutRequestsError(MockAPIResponse):
    url = "https://example.com/api/push"
    method = "POST"
    default_exc = requests.exceptions.Timeout


class PushTimeoutHTTPXError(MockAPIResponse):
    url = "https://example.com/api/push"
    method = "POST"
    default_exc = httpx.TimeoutException(
        message="Timeout error",
        request=httpx.Request("POST", "https://example.com/api/push"),
    )


class SecondPush(Push):
    default_json = {
        "id": "push103",
        "message": "Pushed commit102",
        "author": "dev@example.com",
        "timestamp": "2023-11-08T12:34:56Z",
    }


class ForcePush(MockAPIResponse):
    url = "https://example.com/api/force-push"
    method = "POST"
    endpoint_name = "ForcePush"
    default_status_code = 200
    default_json = {
        "id": "push102",
        "message": "Pushed commit102",
        "author": "dev@example.com",
        "timestamp": "2023-11-08T12:34:56Z",
    }
