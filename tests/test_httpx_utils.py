from unittest.mock import Mock
import pytest
from multi_api_mocker.httpx_utils import HTTPXMockSet
from multi_api_mocker.definitions import MockAPIResponse


def test_httpx_mock_set():
    mock_response = MockAPIResponse(endpoint_name="test", url="https://example.com")
    mock_set = HTTPXMockSet([mock_response], Mock())
    assert len(mock_set) == 1
    assert mock_set["test"] == mock_response
    assert list(mock_set) == [mock_response]
    assert repr(mock_set) == "<HTTPXMockSet with endpoints: test>"
    assert mock_set.get_matcher("https://example.com") is not None


def test_httpx_mock_set_with_empty_list():
    mock_set = HTTPXMockSet([], Mock())
    assert len(mock_set) == 0
    assert list(mock_set) == []
    assert repr(mock_set) == "<HTTPXMockSet with endpoints: >"


def test_get_request():
    mock_response = MockAPIResponse(endpoint_name="test", url="https://example.com")
    mock_httpx = Mock()
    mock_httpx.get_requests.return_value = [Mock(url="https://example.com")]
    mock_set = HTTPXMockSet([mock_response], mock_httpx)
    assert mock_set.get_request("test") is not None


def test_get_request_not_found():
    mock_response = MockAPIResponse(endpoint_name="test", url="https://example.com")
    mock_httpx = Mock()
    mock_httpx.get_requests.return_value = []
    mock_set = HTTPXMockSet([mock_response], mock_httpx)
    with pytest.raises(KeyError):
        mock_set.get_request("test")