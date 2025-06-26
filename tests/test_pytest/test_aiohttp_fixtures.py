import pytest
from aiohttp import ClientSession
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
