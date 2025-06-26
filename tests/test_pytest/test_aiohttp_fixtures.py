import pytest
from aiohttp import ClientSession, client_exceptions
from multi_api_mocker.definitions import MockAPIResponse


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
        with pytest.raises(client_exceptions.ClientConnectorError):
            await session.get("https://example.com/api/error")
