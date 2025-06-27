from typing import List, Callable
from aioresponses import aioresponses
from multi_api_mocker.definitions import MockAPIResponse


class MockAIOAPIResponse(MockAPIResponse):
    """
    A specialized MockAPIResponse for aiohttp with advanced features.

    This class extends MockAPIResponse to include support for aioresponses-specific
    features such as custom headers, raw body content, and dynamic callbacks. It ensures
    that advanced features are only used with this specialized class, raising a
    TypeError if they are attempted with the base MockAPIResponse.

    Attributes:
        default_headers (dict): Default headers for the response.
        default_body (bytes): Default body for the response.
        default_callback (Callable): Default callback for the response.
    """

    default_headers: dict | None = None
    default_body: bytes | None = None
    default_callback: Callable | None = None

    def __init__(
        self,
        *args,
        headers=None,
        body=None,
        callback=None,
        **kwargs,
    ):
        """
        Initializes the MockAIOAPIResponse with advanced options.

        Args:
            headers (dict, optional): The headers of the response.
            body (bytes, optional): The body of the response.
            callback (Callable, optional): The callback to execute.
            **kwargs: Additional keyword arguments for the base class.
        """
        super().__init__(*args, **kwargs)
        self._headers = headers
        self._body = body
        self._callback = callback

        if (headers or body or callback) and not isinstance(self, MockAIOAPIResponse):
            raise TypeError(
                "Advanced features like headers, body, and callback are only "
                "available with MockAIOAPIResponse."
            )

    @property
    def headers(self):
        return self._headers or self.__class__.default_headers

    @property
    def body(self):
        return self._body or self.__class__.default_body

    @property
    def callback(self):
        return self._callback or self.__class__.default_callback


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