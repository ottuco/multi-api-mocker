from typing import List
from aioresponses import aioresponses
from multi_api_mocker.definitions import MockAPIResponse


class AIOHTTPMockSet:
    """
    A collection class that manages MockAPIResponse objects and integrates with the
    aioresponses fixture. This class provides efficient access and iteration over
    grouped API responses by their endpoint names, simplifying the process of setting
    up and managing multiple mock responses in tests for aiohttp.
    """

    def __init__(
        self,
        api_responses: List[MockAPIResponse],
        aiohttp_mock: aioresponses,
    ):
        self._response_registry = {
            response.endpoint_name: response for response in api_responses
        }
        self.aiohttp_mock = aiohttp_mock

    def __getitem__(self, endpoint_name: str) -> MockAPIResponse:
        return self._response_registry[endpoint_name]

    def __iter__(self):
        return iter(self._response_registry.values())

    def __len__(self):
        return len(self._response_registry)

    def __repr__(self):
        endpoint_names = ", ".join(self._response_registry.keys())
        return f"<{self.__class__.__name__} with endpoints: {endpoint_names}>"
