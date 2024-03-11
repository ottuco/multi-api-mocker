from multi_api_mocker.definitions import MockAPIResponse
from multi_api_mocker.models import MockConfiguration, ResponseKwargs
from multi_api_mocker.http_utils import group_by_url


# Test grouping with a single mock


def test_group_by_url_single_mock():
    mock_response = MockAPIResponse(
        url="https://example.com/api",
        method="GET",
        status_code=200,
        json={"key": "value"},
    )
    # Create an instance of ResponseKwargs
    response_kwargs = ResponseKwargs(status_code=200, json={"key": "value"})
    expected = [
        MockConfiguration(
            url="https://example.com/api",
            method="GET",
            responses=[
                response_kwargs.to_dict()  # Convert to dictionary using to_dict()
            ],
        )
    ]
    assert group_by_url([mock_response]) == expected


# Test grouping with multiple mocks for the same endpoint
def test_group_by_url_multiple_mocks_same_endpoint():
    mock_responses = [
        MockAPIResponse(
            url="https://example.com/api",
            method="GET",
            status_code=200,
            json={"key": "value1"},
        ),
        MockAPIResponse(
            url="https://example.com/api",
            method="GET",
            status_code=404,
            json={"key": "value2"},
        ),
    ]
    expected = [
        MockConfiguration(
            url="https://example.com/api",
            method="GET",
            responses=[
                {"status_code": 200, "json": {"key": "value1"}},
                {"status_code": 404, "json": {"key": "value2"}},
            ],
        )
    ]
    assert group_by_url(mock_responses) == expected


# Test grouping with a mock that raises an exception
def test_group_by_url_with_exception():
    mock_responses = [
        MockAPIResponse(url="https://example.com/api", method="GET", exc=Exception)
    ]
    expected = [
        MockConfiguration(
            url="https://example.com/api",
            method="GET",
            responses=[{"exc": Exception}],
        )
    ]
    assert group_by_url(mock_responses) == expected


# Test grouping with mocks for different HTTP methods
def test_group_by_url_multiple_methods():
    mock_responses = [
        MockAPIResponse(
            url="https://example.com/api",
            method="GET",
            status_code=200,
            json={"key": "value"},
        ),
        MockAPIResponse(
            url="https://example.com/api",
            method="POST",
            status_code=201,
            json={"key": "value"},
        ),
    ]
    expected = [
        MockConfiguration(
            url="https://example.com/api",
            method="GET",
            responses=[{"status_code": 200, "json": {"key": "value"}}],
        ),
        MockConfiguration(
            url="https://example.com/api",
            method="POST",
            responses=[{"status_code": 201, "json": {"key": "value"}}],
        ),
    ]
    assert group_by_url(mock_responses) == expected
