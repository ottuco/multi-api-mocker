import pytest
from unittest.mock import Mock, patch
import requests
import httpx
import aiohttp
import sys
import importlib
from multi_api_mocker.contrib.pytest_plugin import (
    setup_api_mocks,
    setup_http_mocks,
    setup_httpx_mocks,
    setup_aiohttp_mocks,
    add_response,
    add_aiohttp_response,
)
from multi_api_mocker.definitions import MockAPIResponse


@pytest.mark.parametrize(
    "setup_api_mocks",
    [[MockAPIResponse(url="https://example.com", method="GET")]],
    indirect=True,
)
def test_setup_api_mocks_deprecation_warning(setup_api_mocks):
    requests.get("https://example.com")


@pytest.mark.parametrize(
    "setup_http_mocks",
    [[MockAPIResponse(url="https://example.com", method="GET")]],
    indirect=True,
)
def test_setup_http_mocks(setup_http_mocks):
    requests.get("https://example.com")
    assert setup_http_mocks is not None


@pytest.mark.parametrize(
    "setup_httpx_mocks",
    [[MockAPIResponse(url="https://example.com", method="GET")]],
    indirect=True,
)
def test_setup_httpx_mocks(setup_httpx_mocks):
    with httpx.Client() as client:
        client.get("https://example.com")
    assert setup_httpx_mocks is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "setup_aiohttp_mocks",
    [[MockAPIResponse(url="https://example.com", method="GET", status_code=200)]],
    indirect=True,
)
async def test_setup_aiohttp_mocks(setup_aiohttp_mocks):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://example.com") as response:
            assert response.status == 200
    assert setup_aiohttp_mocks is not None


@pytest.mark.parametrize(
    "setup_httpx_mocks",
    [
        [
            [
                MockAPIResponse(url="https://example.com", method="GET"),
                MockAPIResponse(url="https://example.com", method="GET"),
            ]
        ]
    ],
    indirect=True,
)
def test_setup_httpx_mocks_with_nested_list(setup_httpx_mocks):
    with httpx.Client() as client:
        client.get("https://example.com")
        client.get("https://example.com")
    assert setup_httpx_mocks is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "setup_aiohttp_mocks",
    [
        [
            [
                MockAPIResponse(
                    url="https://example.com", method="GET", status_code=200
                ),
                MockAPIResponse(
                    url="https://example.com", method="GET", status_code=200
                ),
            ]
        ]
    ],
    indirect=True,
)
async def test_setup_aiohttp_mocks_with_nested_list(setup_aiohttp_mocks):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://example.com") as response:
            assert response.status == 200
        async with session.get("https://example.com") as response:
            assert response.status == 200
    assert setup_aiohttp_mocks is not None


def test_add_response_invalid_type():
    with pytest.raises(ValueError):
        add_response(Mock(), "not a mock")


def test_add_aiohttp_response_invalid_type():
    with pytest.raises(ValueError):
        add_aiohttp_response(Mock(), "not a mock")


def test_import_error_requests_mock():
    with patch.dict("sys.modules", {"requests_mock": None}):
        import multi_api_mocker.contrib.pytest_plugin as pytest_plugin
        importlib.reload(pytest_plugin)
        assert not pytest_plugin.requests_mock_available


def test_import_error_httpx():
    with patch.dict("sys.modules", {"pytest_httpx": None}):
        import multi_api_mocker.contrib.pytest_plugin as pytest_plugin
        importlib.reload(pytest_plugin)
        assert not pytest_plugin.httpx_available


def test_import_error_aiohttp():
    with patch.dict("sys.modules", {"aioresponses": None}):
        import multi_api_mocker.contrib.pytest_plugin as pytest_plugin
        importlib.reload(pytest_plugin)
        assert not pytest_plugin.aiohttp_available