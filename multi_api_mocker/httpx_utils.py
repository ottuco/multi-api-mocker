from typing import List

from httpx import Request
from pytest_httpx import HTTPXMock

from multi_api_mocker.definitions import MockAPIResponse


class HTTPXMockSet:
    """
    A collection class that manages MockAPIResponse objects and integrates with the
    httpx_mock fixture from the pytest-httpx library. This class provides efficient
    access and iteration over grouped API responses by their endpoint names,
    simplifying the process of setting up and managing multiple mock responses in tests.

    Unlike the RequestsMockSet, which works with requests_mock, the HTTPXMockSet behaves
    differently because httpx_mock does not create requests until they are actually
    executed during the test. As a result, some methods that rely on accessing the
    requests before execution may not work as expected.

    Parameters:
        api_responses (List[MockAPIResponse]): A list of MockAPIResponse objects, each
                                               representing a specific API response.
        httpx_mock (HTTPXMock): The httpx_mock fixture instance used for registering
                                the mock API responses.

    Attributes:
        _response_registry (Dict[str, MockAPIResponse]): A dictionary mapping endpoint
                                                         names to their respective
                                                         MockAPIResponse objects.
        httpx_mock (HTTPXMock): The httpx_mock fixture instance.

    Methods:
        get_request(endpoint_name: str) -> Request: Retrieves the httpx Request object
                                                    associated with the given endpoint
                                                    name after the mock has been
                                                    executed.
    """

    def __init__(
        self,
        api_responses: List[MockAPIResponse],
        httpx_mock: HTTPXMock,
    ):
        self._response_registry = {
            response.endpoint_name: response for response in api_responses
        }
        self.httpx_mock = httpx_mock

    def __getitem__(self, endpoint_name: str) -> MockAPIResponse:
        return self._response_registry[endpoint_name]

    def __iter__(self):
        return iter(self._response_registry.values())

    def __len__(self):
        return len(self._response_registry)

    def __repr__(self):
        endpoint_names = ", ".join(self._response_registry.keys())
        return f"<{self.__class__.__name__} with endpoints: {endpoint_names}>"

    def get_request(self, endpoint_name: str) -> Request:
        """
        Retrieves the httpx Request object associated with the given endpoint name
        after the mock has been executed.

        Parameters:
            endpoint_name (str): The name of the endpoint to retrieve the request for.

        Returns:
            Request: The httpx Request object associated with the given endpoint name.

        Raises:
            KeyError: If no request is found for the given endpoint name.
        """
        for request in self.httpx_mock.get_requests():
            if request.url == self._response_registry[endpoint_name].url:
                return request
        raise KeyError(f"No request found for endpoint: {endpoint_name}")
