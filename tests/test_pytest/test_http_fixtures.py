import pytest
import requests
from requests import RequestException

from multi_api_mocker.definitions import MockAPIResponse
from . import mocks


@pytest.mark.parametrize(
    "setup_http_mocks",
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
def test_commit_and_push(setup_http_mocks):
    # Perform the commit API call
    commit_response = requests.post("https://example.com/api/commit")
    assert commit_response.json() == {
        "message": "Commit successful",
        "commit_id": "abc123",
    }

    # Perform the push API call
    push_response = requests.post("https://example.com/api/push")
    assert push_response.json() == {"message": "Push successful", "push_id": "xyz456"}


@pytest.mark.parametrize(
    "setup_http_mocks",
    [
        [
            mocks.Fork(),
            mocks.Commit(),
            mocks.Push(),
        ]
    ],
    indirect=True,
)
def test_single_flow_multiple_api_calls(setup_http_mocks):
    mock_set = setup_http_mocks
    # Perform the API call
    response = requests.post("https://example.com/api/fork")

    # Assert the response matches what was defined in the Fork mock
    assert response.json() == mock_set["Fork"].json

    response = requests.get("https://example.com/api/commit")
    assert response.json() == mock_set["Commit"].json

    response = requests.post("https://example.com/api/push")
    assert response.json() == mock_set["Push"].json


@pytest.mark.parametrize(
    "setup_http_mocks",
    [
        # Scenario 1: Push fails with a 400 error
        (
            [
                mocks.Fork(),
                mocks.Commit(),
                mocks.Push(status_code=400, json={"error": "Push failed"}),
            ]
        ),
        # Scenario 2: Force push succeeds after a failed push
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
def test_multiple_scenarios(setup_http_mocks):
    mock_set = setup_http_mocks
    # Perform the API call
    response = requests.post("https://example.com/api/fork")

    # Assert the response matches what was defined in the Fork mock
    assert response.json() == mock_set["Fork"].json

    response = requests.get("https://example.com/api/commit")
    assert response.json() == mock_set["Commit"].json

    response = requests.post("https://example.com/api/push")
    assert response.status_code == 400
    assert response.json() == mock_set["Push"].json

    if "ForcePush" in mock_set:
        response = requests.post("https://example.com/api/force-push")
        assert response.json() == mock_set["ForcePush"].json


@pytest.mark.parametrize(
    "setup_http_mocks",
    [
        # Scenario 1: Push fails with a 400 error
        (
            [
                mocks.Fork(),
                mocks.Commit(),
                mocks.Push(exc=RequestException),
            ]
        ),
        # Scenario 2: Force fails with 400 using `default_exc`
        (
            [
                mocks.Fork(),
                mocks.Commit(),
                mocks.PushTimeoutRequestsError(),
            ]
        ),
    ],
    indirect=True,
)
def test_exception(setup_http_mocks):
    mock_set = setup_http_mocks
    # Perform the API call
    response = requests.post("https://example.com/api/fork")

    # Assert the response matches what was defined in the Fork mock
    assert response.json() == mock_set["Fork"].json

    response = requests.get("https://example.com/api/commit")
    assert response.json() == mock_set["Commit"].json

    with pytest.raises(RequestException):
        requests.post("https://example.com/api/push")


@pytest.mark.parametrize(
    "setup_http_mocks",
    [
        ([mocks.Fork(), mocks.Commit(), mocks.Push(partial_json={"id": "partial_id"})]),
    ],
    indirect=True,
)
def test_partial_json(setup_http_mocks):
    mock_set = setup_http_mocks

    response = requests.post("https://example.com/api/push")
    expected_json = mock_set["Push"].json
    expected_json["id"] = "partial_id"

    assert response.status_code == 200
    assert response.json() == expected_json


@pytest.mark.parametrize(
    "user_email, setup_http_mocks",
    [
        ("dev1@example.com", [mocks.Fork(), mocks.Commit(), mocks.Push()]),
        (
            "dev2@example.com",
            [
                mocks.Fork(),
                mocks.Commit(),
                mocks.Push(json={"message": "Pushed with different user"}),
            ],
        ),
    ],
    indirect=["setup_http_mocks"],
)
def test_flexible_parametrization(user_email, setup_http_mocks):
    mock_set = setup_http_mocks

    response = requests.post("https://example.com/api/push", json={"email": user_email})
    expected_json = mock_set["Push"].json

    assert response.status_code == 200
    assert response.json() == expected_json


@pytest.mark.parametrize(
    "setup_http_mocks",
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
def test_same_endpoint_url(setup_http_mocks):
    mock_set = setup_http_mocks

    response = requests.post("https://example.com/api/push")
    assert response.json() == mock_set["Push"].json

    response2 = requests.post("https://example.com/api/push")
    assert response2.json() == mock_set["SecondPush"].json

    matcher = mock_set.get_matcher("https://example.com/api/push")
    assert matcher == mock_set.get_matcher(mock_set["Push"].url)

    assert matcher.call_count == 2


@pytest.mark.parametrize(
    "setup_http_mocks",
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
def test_http_mocking_with_headers(setup_http_mocks):
    response = requests.get("https://example.com/api/test_headers")
    assert response.status_code == 200
    assert response.json() == {"message": "Success"}
    assert response.headers["X-Custom-Header"] == "Test-Value"


def callback_test(request, context):
    context.status_code = 200
    context.headers["X-Callback-Header"] = "Callback-Value"
    return {"message": "Callback executed"}


@pytest.mark.parametrize(
    "setup_http_mocks",
    [
        [
            MockAPIResponse(
                url="https://example.com/api/test_callback",
                method="GET",
                json=callback_test,
            )
        ]
    ],
    indirect=True,
)
def test_http_mocking_with_callback(setup_http_mocks):
    response = requests.get("https://example.com/api/test_callback")
    assert response.status_code == 200
    assert response.json() == {"message": "Callback executed"}
    assert response.headers["X-Callback-Header"] == "Callback-Value"