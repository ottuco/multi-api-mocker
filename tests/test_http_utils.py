from unittest.mock import Mock
import pytest
from multi_api_mocker.http_utils import RequestsMockSet, group_by_url, add_mock_to_group
from multi_api_mocker.definitions import MockAPIResponse
from collections import defaultdict


def test_requests_mock_set():
    mock_response = MockAPIResponse(endpoint_name="test")
    mock_set = RequestsMockSet([mock_response], Mock(), {"test": "matcher"})
    assert len(mock_set) == 1
    assert mock_set["test"] == mock_response
    assert list(mock_set) == [mock_response]
    assert repr(mock_set) == "<RequestsMockSet with endpoints: test>"
    assert mock_set.get_matcher("test") == "matcher"


def test_requests_mock_set_with_empty_list():
    mock_set = RequestsMockSet([], Mock())
    assert len(mock_set) == 0
    assert list(mock_set) == []
    assert repr(mock_set) == "<RequestsMockSet with endpoints: >"


def test_group_by_url():
    mock_response_1 = MockAPIResponse(
        url="https://example.com", method="GET", json={"foo": "bar"}
    )
    mock_response_2 = MockAPIResponse(
        url="https://example.com", method="GET", json={"foo": "baz"}
    )
    mock_response_3 = MockAPIResponse(
        url="https://example.com", method="POST", json={"foo": "bar"}
    )
    mock_response_4 = MockAPIResponse(
        url="https://example.com/2", method="GET", json={"foo": "bar"}
    )
    mock_response_5 = MockAPIResponse(
        url="https://example.com/2", method="GET", exc=Exception
    )

    grouped = group_by_url(
        [
            mock_response_1,
            mock_response_2,
            mock_response_3,
            mock_response_4,
            mock_response_5,
        ]
    )
    assert len(grouped) == 3
    assert grouped[0].url == "https://example.com"
    assert grouped[0].method == "GET"
    assert len(grouped[0].responses) == 2
    assert grouped[1].url == "https://example.com"
    assert grouped[1].method == "POST"
    assert len(grouped[1].responses) == 1
    assert grouped[2].url == "https://example.com/2"
    assert grouped[2].method == "GET"
    assert len(grouped[2].responses) == 2


def test_group_by_url_with_nested_list():
    mock_response_1 = MockAPIResponse(
        url="https://example.com", method="GET", json={"foo": "bar"}
    )
    mock_response_2 = MockAPIResponse(
        url="https://example.com", method="GET", json={"foo": "baz"}
    )
    grouped = group_by_url([[mock_response_1, mock_response_2]])
    assert len(grouped) == 1
    assert grouped[0].url == "https://example.com"
    assert grouped[0].method == "GET"
    assert len(grouped[0].responses) == 2


def test_group_by_url_with_invalid_type():
    with pytest.raises(ValueError):
        group_by_url(["not a mock"])


def test_group_by_url_with_nested_invalid_type():
    with pytest.raises(ValueError):
        group_by_url([["not a mock"]])


def test_add_mock_to_group():
    grouped_mocks = defaultdict(list)
    mock = MockAPIResponse(
        url="https://example.com",
        method="GET",
        json={"foo": "bar"},
        text="test",
        status_code=200,
        exc=Exception,
        headers={"X-Custom-Header": "Test-Value"},
    )
    add_mock_to_group(grouped_mocks, mock)
    assert len(grouped_mocks) == 1
    assert len(grouped_mocks[("https://example.com", "GET")]) == 1
