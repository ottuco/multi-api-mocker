import warnings
from typing import Union, List

import pytest

from ..definitions import MockAPIResponse


try:
    from requests_mock import Mocker  # type: ignore # noqa: F401
    from ..http_utils import group_by_url, RequestsMockSet  # noqa: F401

    requests_mock_available = True
except ImportError:
    requests_mock_available = False

try:
    from pytest_httpx import HTTPXMock  # type: ignore # noqa: F401
    from ..httpx_utils import HTTPXMockSet  # noqa: F401

    httpx_available = True
except ImportError:
    httpx_available = False

if requests_mock_available:

    @pytest.fixture(scope="function")
    def setup_http_mocks(requests_mock: Mocker, request) -> RequestsMockSet:
        """
        A pytest fixture for configuring mock HTTP responses in a test environment.
        It takes subclasses of MockAPIResponse, each representing a unique API call
        configuration. These subclasses facilitate the creation of simple or complex
        response flows, simulating real-world API interactions.

        Parameters:
            requests_mock (Mocker): The pytest requests_mock fixture.
            request: The pytest request object containing parametrized test data.

        Returns:
            RequestsMockSet: An instance of MockSet containing the organized
                    MockAPIResponse objects, ready for use in tests.

        The fixture supports multiple test scenarios, allowing for thorough
        testing of varying API response conditions. This is especially useful
        for simulating sequences of API calls like Fork, Commit, and Push
        in a version control system context.

        Example Usage:
            - Single API Call Test:
              @pytest.mark.parametrize("setup_http_mocks", [([Fork()])], indirect=True)

            - Multi-call Sequence Test:
              @pytest.mark.parametrize(
                  "setup_http_mocks", [([Fork(), Commit(), Push()])], indirect=True
              )

            - Testing Multiple Scenarios:
            @pytest.mark.parametrize(
                "setup_http_mocks",
                [([Fork(), Commit(), Push()]), ([Fork(), Commit(), ForcePush()])],
                indirect=True
            )


        This fixture converts the list of MockAPIResponse subclasses into
        MockConfiguration instances, registers them with requests_mock,
        and returns a MockSet object, which allows querying each mock
        by its endpoint name.
        """
        yield from configure_http_mocks(requests_mock, request)

    # Deprecated wrapper fixture
    @pytest.fixture(scope="function")
    def setup_api_mocks(requests_mock: Mocker, request) -> RequestsMockSet:
        """
        Deprecated: Use `setup_http_mocks` instead.
        """
        warnings.warn(
            "`setup_api_mocks` is deprecated and will be removed in a future release. "
            "Please use `setup_http_mocks` instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        yield from configure_http_mocks(requests_mock, request)

    def configure_http_mocks(requests_mock: Mocker, request):
        api_mocks_configurations = group_by_url(request.param)
        matchers = {}

        for api_mock in api_mocks_configurations:
            matcher = requests_mock.register_uri(
                api_mock.method, api_mock.url, api_mock.responses
            )
            matchers[api_mock.url] = matcher

        yield RequestsMockSet(request.param, requests_mock, matchers)


if httpx_available:

    @pytest.fixture(scope="function")
    def setup_httpx_mocks(httpx_mock: HTTPXMock, request) -> HTTPXMockSet:
        """
        A pytest fixture for configuring mock HTTPX responses in a test environment.
        Directly registers each mock response for HTTPX, leveraging pytest-httpx's
        ability to queue multiple responses for the same URL and method.

        Parameters:
            httpx_mock (HTTPXMock): The pytest-httpx fixture for mocking HTTPX requests.
            request: The pytest request object containing parameterized test data.

        Returns:
            HTTPXMockSet: An instance of HttpxMockSet containing the organized
                          MockAPIResponse objects, ready for use in tests.

        Usage in tests is similar to the original setup_api_mocks, using pytest's
        parametrize decorator to supply mock response definitions.
        """
        mock_definitions: List[
            Union[MockAPIResponse, List[MockAPIResponse]]
        ] = request.param

        for mock_definition in mock_definitions:
            if isinstance(mock_definition, list):
                for nested_mock_definition in mock_definition:
                    add_response(httpx_mock, nested_mock_definition)
            else:
                add_response(httpx_mock, mock_definition)

        yield HTTPXMockSet(mock_definitions, httpx_mock)

    def add_response(httpx_mock: HTTPXMock, mock_definition: MockAPIResponse):
        if not isinstance(mock_definition, MockAPIResponse):
            raise ValueError(
                f"Unsupported mock definition type: {type(mock_definition)}"
            )
        if mock_definition.exc:
            httpx_mock.add_exception(
                url=mock_definition.url,
                method=mock_definition.method,
                exception=mock_definition.exc,
            )
        else:
            httpx_mock.add_response(
                url=mock_definition.url,
                method=mock_definition.method,
                json=mock_definition.json,
                status_code=mock_definition.status_code,
            )
