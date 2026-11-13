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

try:
    from aioresponses import aioresponses  # type: ignore # noqa: F401
    from ..aiohttp_utils import AIOHTTPMockSet  # noqa: F401

    aiohttp_available = True
except ImportError:
    aiohttp_available = False


if requests_mock_available:

    @pytest.fixture(scope="function")
    def setup_http_mocks(requests_mock: Mocker, request) -> RequestsMockSet:
        if not requests_mock_available:
            pytest.skip("requests-mock is not installed")
        yield from configure_http_mocks(requests_mock, request)

    # Deprecated wrapper fixture
    @pytest.fixture(scope="function")
    def setup_api_mocks(requests_mock: Mocker, request) -> RequestsMockSet:
        if not requests_mock_available:
            pytest.skip("requests-mock is not installed")
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
            responses = []
            for response in api_mock.responses:
                response_data = {
                    key: response.get(key)
                    for key in ("json", "status_code", "headers", "exc")
                    if response.get(key) is not None
                }
                if response.get("callback") is not None:
                    response_data["json"] = response.get("callback")
                responses.append(response_data)
            matcher = requests_mock.register_uri(
                api_mock.method,
                api_mock.url,
                response_list=responses,
            )
            matchers[api_mock.url] = matcher

        yield RequestsMockSet(request.param, requests_mock, matchers)


if httpx_available:

    @pytest.fixture(scope="function")
    def setup_httpx_mocks(httpx_mock: HTTPXMock, request) -> HTTPXMockSet:
        if not httpx_available:
            pytest.skip("pytest-httpx is not installed")
        mock_definitions: List[Union[MockAPIResponse, List[MockAPIResponse]]] = (
            request.param
        )
        flattened_definitions = []
        for mock_definition in mock_definitions:
            if isinstance(mock_definition, list):
                flattened_definitions.extend(mock_definition)
            else:
                flattened_definitions.append(mock_definition)

        for mock_definition in flattened_definitions:
            add_response(httpx_mock, mock_definition)

        yield HTTPXMockSet(flattened_definitions, httpx_mock)

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
        elif mock_definition.callback:
            httpx_mock.add_callback(
                url=mock_definition.url,
                method=mock_definition.method,
                callback=mock_definition.callback,
            )
        else:
            httpx_mock.add_response(
                url=mock_definition.url,
                method=mock_definition.method,
                json=mock_definition.json,
                text=mock_definition.text,
                status_code=mock_definition.status_code,
                headers=mock_definition.headers,
            )


if aiohttp_available:

    @pytest.fixture
    def setup_aiohttp_mocks(request) -> AIOHTTPMockSet:
        if not aiohttp_available:
            pytest.skip("aioresponses is not installed")
        with aioresponses() as m:
            mock_definitions: List[Union[MockAPIResponse, List[MockAPIResponse]]] = (
                request.param
            )
            flattened_definitions = []
            for mock_definition in mock_definitions:
                if isinstance(mock_definition, list):
                    flattened_definitions.extend(mock_definition)
                else:
                    flattened_definitions.append(mock_definition)

            for mock_definition in flattened_definitions:
                add_aiohttp_response(m, mock_definition)

            yield AIOHTTPMockSet(flattened_definitions, m)

    def add_aiohttp_response(
        aiohttp_mock: aioresponses, mock_definition: MockAPIResponse
    ):
        if not isinstance(mock_definition, MockAPIResponse):
            raise ValueError(
                f"Unsupported mock definition type: {type(mock_definition)}"
            )
        if mock_definition.exc:
            aiohttp_mock.add(
                url=mock_definition.url,
                method=mock_definition.method.upper(),
                exception=mock_definition.exc,
            )
        else:
            aiohttp_mock.add(
                url=mock_definition.url,
                method=mock_definition.method.upper(),
                payload=mock_definition.json,
                status=mock_definition.status_code,
                headers=mock_definition.headers,
                callback=mock_definition.callback,
            )
