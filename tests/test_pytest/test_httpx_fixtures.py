import httpx
import pytest

from multi_api_mocker.definitions import MockAPIResponse
from . import mocks


@pytest.mark.parametrize(
    "setup_httpx_mocks",
    [
        [
            MockAPIResponse(
                url="https://example.com/api/commit",
                method="POST",
                json={"message": "Commit successful", "commit_id": "abc123"},
            ),
            MockAPIResponse(
                url="https://example.com/api/push",
                method="POST",
                json={"message": "Push successful", "push_id": "xyz456"},
            ),
        ]
    ],
    indirect=True,
)
def test_commit_and_push(setup_httpx_mocks):
    # Perform the commit API call
    with httpx.Client() as client:
        commit_response = client.post("https://example.com/api/commit")
        assert commit_response.json() == {
            "message": "Commit successful",
            "commit_id": "abc123",
        }

        # Perform the push API call
        push_response = client.post("https://example.com/api/push")
        assert push_response.json() == {
            "message": "Push successful",
            "push_id": "xyz456",
        }


@pytest.mark.parametrize(
    "setup_httpx_mocks",
    [
        [
            mocks.Fork(),
            mocks.Commit(),
            mocks.Push(),
        ]
    ],
    indirect=True,
)
def test_single_flow_multiple_api_calls(setup_httpx_mocks):
    mock_set = setup_httpx_mocks
    # Perform the API call
    with httpx.Client() as client:
        response = client.post("https://example.com/api/fork")

        # Assert the response matches what was defined in the Fork mock
        assert response.json() == mock_set["Fork"].json

        response = client.get("https://example.com/api/commit")
        assert response.json() == mock_set["Commit"].json

        response = client.post("https://example.com/api/push")
        assert response.json() == mock_set["Push"].json


@pytest.mark.parametrize(
    "setup_httpx_mocks",
    [
        (
            [
                mocks.Fork(),
                mocks.Commit(),
                mocks.Push(status_code=400, json={"error": "Push failed"}),
            ]
        ),
    ],
    indirect=True,
)
def test_multiple_scenarios_push_fails(setup_httpx_mocks):
    mock_set = setup_httpx_mocks
    # Perform the API call
    with httpx.Client() as client:
        response = client.post("https://example.com/api/fork")

        # Assert the response matches what was defined in the Fork mock
        assert response.json() == mock_set["Fork"].json

        response = client.get("https://example.com/api/commit")
        assert response.json() == mock_set["Commit"].json

        response = client.post("https://example.com/api/push")
        assert response.status_code == 400
        assert response.json() == mock_set["Push"].json

        with pytest.raises(httpx.TimeoutException):
            client.post("https://example.com/api/force-push")


@pytest.mark.parametrize(
    "setup_httpx_mocks",
    [
        (
            [
                mocks.Fork(),
                mocks.Commit(),
                mocks.Push(status_code=400, json={"error": "Push failed"}),
                mocks.ForcePush(),
            ]
        ),
    ],
    indirect=True,
)
def test_multiple_scenarios_force_push_succeeds(setup_httpx_mocks):
    mock_set = setup_httpx_mocks
    # Perform the API call
    with httpx.Client() as client:
        response = client.post("https://example.com/api/fork")

        # Assert the response matches what was defined in the Fork mock
        assert response.json() == mock_set["Fork"].json

        response = client.get("https://example.com/api/commit")
        assert response.json() == mock_set["Commit"].json

        response = client.post("https://example.com/api/push")
        assert response.status_code == 400
        assert response.json() == mock_set["Push"].json

        response = client.post("https://example.com/api/force-push")
        assert response.json() == mock_set["ForcePush"].json


@pytest.mark.parametrize(
    "setup_httpx_mocks",
    [
        # Scenario 1: Push fails with a 400 error
        (
            [
                mocks.Fork(),
                mocks.Commit(),
                mocks.Push(
                    exc=httpx.RequestError(
                        "Request error",
                        request=httpx.Request("POST", "https://example.com/api/push"),
                    )
                ),
            ]
        ),
        # Scenario 2: Force fails with 400 using `default_exc`
        (
            [
                mocks.Fork(),
                mocks.Commit(),
                mocks.PushTimeoutHTTPXError(),
            ]
        ),
    ],
    indirect=True,
)
def test_exception(setup_httpx_mocks):
    mock_set = setup_httpx_mocks
    # Perform the API calls
    with httpx.Client() as client:
        response = client.post("https://example.com/api/fork")

        # Assert the response matches what was defined in the Fork mock
        assert response.json() == mock_set["Fork"].json

        response = client.get("https://example.com/api/commit")
        assert response.json() == mock_set["Commit"].json

        with pytest.raises(httpx.RequestError):
            client.post("https://example.com/api/push")


@pytest.mark.parametrize(
    "setup_httpx_mocks",
    [
        ([mocks.Push(partial_json={"id": "partial_id"})]),
    ],
    indirect=True,
)
def test_partial_json(setup_httpx_mocks):
    mock_set = setup_httpx_mocks

    with httpx.Client() as client:
        response = client.post("https://example.com/api/push")
        expected_json = mock_set["Push"].json
        expected_json["id"] = "partial_id"

        assert response.status_code == 200
        assert response.json() == expected_json


@pytest.mark.parametrize(
    "user_email, setup_httpx_mocks",
    [
        ("dev1@example.com", [mocks.Push()]),
        (
            "dev2@example.com",
            [
                mocks.Push(json={"message": "Pushed with different user"}),
            ],
        ),
    ],
    indirect=["setup_httpx_mocks"],
)
def test_flexible_parametrization(user_email, setup_httpx_mocks):
    mock_set = setup_httpx_mocks

    with httpx.Client() as client:
        response = client.post(
            "https://example.com/api/push", json={"email": user_email}
        )
        expected_json = mock_set["Push"].json

        assert response.status_code == 200
        assert response.json() == expected_json


@pytest.mark.parametrize(
    "setup_httpx_mocks",
    [
        (
            [
                mocks.Push(),
                mocks.SecondPush(),
            ]
        ),
    ],
    indirect=True,
)
def test_same_endpoint_url(setup_httpx_mocks):
    mock_set = setup_httpx_mocks

    with httpx.Client() as client:
        response = client.post("https://example.com/api/push")
        assert response.json() == mock_set["Push"].json

        response2 = client.post("https://example.com/api/push")
        assert response2.json() == mock_set["SecondPush"].json

        matcher = mock_set.get_matcher("https://example.com/api/push")
        assert matcher == mock_set.get_matcher(mock_set["Push"].url)

        assert len(mock_set.httpx_mock.get_requests()) == 2


@pytest.mark.parametrize(
    "setup_httpx_mocks",
    [
        [
            MockAPIResponse(
                url="https://example.com/api/test_headers",
                method="GET",
                json={"message": "Success"},
                status_code=200,
                headers={"X-Custom-Header": "Test-Value"},
            )
        ]
    ],
    indirect=True,
)
def test_httpx_mocking_with_headers(setup_httpx_mocks):
    with httpx.Client() as client:
        response = client.get("https://example.com/api/test_headers")
    assert response.status_code == 200
    assert response.json() == {"message": "Success"}
    assert response.headers["X-Custom-Header"] == "Test-Value"


@pytest.mark.parametrize(
    "setup_httpx_mocks",
    [
        [
            MockAPIResponse(
                url="https://example.com/api/test_callback",
                method="GET",
                callback=lambda request: httpx.Response(
                    200, json={"message": "Callback executed"}
                ),
            )
        ]
    ],
    indirect=True,
)
def test_httpx_mocking_with_callback(setup_httpx_mocks):
    with httpx.Client() as client:
        response = client.get("https://example.com/api/test_callback")
    assert response.status_code == 200
    assert response.json() == {"message": "Callback executed"}


@pytest.mark.parametrize(
    "setup_httpx_mocks",
    [
        [
            MockAPIResponse(
                url="https://example.com/api/test_callback_headers",
                method="GET",
                callback=lambda request: httpx.Response(
                    200,
                    json={"message": "Callback executed"},
                    headers={"X-Callback-Header": "Callback-Value"},
                ),
            )
        ]
    ],
    indirect=True,
)
def test_httpx_mocking_with_callback_headers(setup_httpx_mocks):
    with httpx.Client() as client:
        response = client.get("https://example.com/api/test_callback_headers")
    assert response.status_code == 200
    assert response.json() == {"message": "Callback executed"}
    assert response.headers["X-Callback-Header"] == "Callback-Value"