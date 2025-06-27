from unittest.mock import Mock
from multi_api_mocker.aiohttp_utils import AIOHTTPMockSet
from multi_api_mocker.definitions import MockAPIResponse


def test_aiohttp_mock_set():
    mock_response = MockAPIResponse(endpoint_name="test")
    mock_set = AIOHTTPMockSet([mock_response], Mock())
    assert len(mock_set) == 1
    assert mock_set["test"] == mock_response
    assert list(mock_set) == [mock_response]
    assert repr(mock_set) == "<AIOHTTPMockSet with endpoints: test>"


def test_aiohttp_mock_set_with_empty_list():
    mock_set = AIOHTTPMockSet([], Mock())
    assert len(mock_set) == 0
    assert list(mock_set) == []
    assert repr(mock_set) == "<AIOHTTPMockSet with endpoints: >"
