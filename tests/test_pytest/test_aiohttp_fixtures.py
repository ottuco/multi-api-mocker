import pytest
from aiohttp import ClientSession
from multi_api_mocker.definitions import MockAPIResponse
from aioresponses import CallbackResult


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "setup_aiohttp_mocks",
    [
        [
            MockAPIResponse(
                url="https://example.com/api/test",
                method="GET",
                json={"message": "Success"},
                status_code=200,
            )
        ]
    ],
    indirect=True,
)
async def test_aiohttp_mocking(setup_aiohttp_mocks):
    async with ClientSession() as session:
        async with session.get("https://example.com/api/test") as response:
            assert response.status == 200
            assert await response.json() == {"message": "Success"}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "setup_aiohttp_mocks",
    [
        [
            MockAPIResponse(
                url="https://example.com/api/error",
                method="GET",
                exc=OSError("Connection refused"),
            )
        ]
    ],
    indirect=True,
)
async def test_aiohttp_exception_mocking(setup_aiohttp_mocks):
    async with ClientSession() as session:
        with pytest.raises(OSError):
            await session.get("https://example.com/api/error")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "setup_aiohttp_mocks",
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
async def test_aiohttp_mocking_with_headers(setup_aiohttp_mocks):
    async with ClientSession() as session:
        async with session.get("https://example.com/api/test_headers") as response:
            assert response.status == 200
            assert await response.json() == {"message": "Success"}
            assert response.headers["X-Custom-Header"] == "Test-Value"


def callback_test(url, **kwargs):
    return CallbackResult(
        status=200,
        payload={"message": "Callback executed"}
    )


def callback_with_headers_test(url, **kwargs):
    return CallbackResult(
        status=200,
        payload={"message": "Callback executed"},
        headers={"X-Callback-Header": "Callback-Value"},
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "setup_aiohttp_mocks",
    [
        [
            MockAPIResponse(
                url="https://example.com/api/test_callback",
                method="GET",
                callback=callback_test,
            )
        ]
    ],
    indirect=True,
)
async def test_aiohttp_mocking_with_callback(setup_aiohttp_mocks):
    async with ClientSession() as session:
        async with session.get("https://example.com/api/test_callback") as response:
            assert response.status == 200
            assert await response.json() == {"message": "Callback executed"}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "setup_aiohttp_mocks",
    [
        [
            MockAPIResponse(
                url="https://example.com/api/test_callback_headers",
                method="GET",
                callback=callback_with_headers_test,
            )
        ]
    ],
    indirect=True,
)
async def test_aiohttp_mocking_with_callback_headers(setup_aiohttp_mocks):
    async with ClientSession() as session:
        async with session.get(
            "https://example.com/api/test_callback_headers"
        ) as response:
            assert response.status == 200
            assert await response.json() == {"message": "Callback executed"}
            assert response.headers["X-Callback-Header"] == "Callback-Value"
