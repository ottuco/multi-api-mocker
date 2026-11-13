# Multi-API Mocker: Streamlined API Mocking for pytest

[![PyPI version](https://img.shields.io/pypi/v/multi-api-mocker.svg)](https://pypi.python.org/pypi/multi-api-mocker)

Multi-API Mocker is a Python utility designed to enhance and simplify the process of mocking multiple API calls in pytest tests. It provides a consistent and intuitive interface for mocking API responses, whether you're using `requests`, `httpx`, or `aiohttp`.

This tool focuses on improving test readability, maintainability, and efficiency in scenarios requiring multiple API interactions, making it an ideal solution for developers and testers who work with complex API testing scenarios in pytest.

## Features

- **Simplified Mock Management**: Organize and manage multiple API mocks in a clean and intuitive way.
- **Enhanced Readability**: Keep your tests neat and readable by separating mock definitions from test logic.
- **Flexible Response Handling**: Easily define and handle different response scenarios for each API endpoint.
- **Seamless Pytest Integration**: Integrates with pytest fixtures, enhancing its capabilities for API mocking.
- **Reduced Boilerplate**: Less repetitive code, focusing only on the specifics of each test case.
- **Customizable Mocks**: Tailor your mocks to fit various testing scenarios with customizable response parameters.

## Installation

Multi-API Mocker offers flexible installation options depending on your project's needs. You can install support for a specific library or all of them for maximum versatility.

- **For `requests` support:**
  ```bash
  pip install multi-api-mocker[http]
  ```

- **For `httpx` support:**
  ```bash
  pip install multi-api-mocker[httpx]
  ```

- **For `aiohttp` support:**
  ```bash
  pip install multi-api-mocker[aiohttp]
  ```

- **For all supported libraries:**
  ```bash
  pip install multi-api-mocker[all]
  ```

## Core Concept: Defining Mock Responses (`MockAPIResponse`)

The foundation of this library is the `MockAPIResponse` class, which serves as a universal blueprint for creating mock responses for your API endpoints, regardless of the underlying HTTP client library. You can use it directly or subclass it to create reusable mock definitions.

### Using `MockAPIResponse` Directly

For simple cases, you can instantiate `MockAPIResponse` directly within your test parametrization.

```python
from multi_api_mocker.definitions import MockAPIResponse

@pytest.mark.parametrize(
    "setup_http_mocks", # Or setup_httpx_mocks, setup_aiohttp_mocks
    [
        ([
            MockAPIResponse(
                url="https://example.com/api/data",
                method="GET",
                json={"message": "Success!"},
                status_code=200
            )
        ])
    ],
    indirect=True
)
def test_direct_mock(setup_http_mocks):
    # Your test logic here
    ...
```

### Subclassing `MockAPIResponse` for Reusability

For more complex or frequently used endpoints, subclassing `MockAPIResponse` is recommended. This enhances reusability and keeps your test definitions clean.

```python
# in tests/mocks.py
from multi_api_mocker.definitions import MockAPIResponse

class UserProfile(MockAPIResponse):
    url = "https://api.example.com/user/profile"
    method = "GET"
    default_status_code = 200
    default_json = {
        "id": "user123",
        "name": "Jane Doe",
        "email": "jane.doe@example.com"
    }

# in your test file
import mocks
import requests # or httpx, aiohttp

def test_user_profile(setup_http_mocks):
    # The mock is already set up by the fixture
    response = requests.get("https://api.example.com/user/profile")
    assert response.json()["name"] == "Jane Doe"

# To override defaults for a specific test:
@pytest.mark.parametrize(
    "setup_http_mocks", # Or setup_httpx_mocks, setup_aiohttp_mocks
    [([
        # Simulate a not found error
        mocks.UserProfile(status_code=404, json={"error": "User not found"})
    ])],
    indirect=True
)
def test_user_not_found(setup_http_mocks):
    response = requests.get("https://api.example.com/user/profile")
    assert response.status_code == 404
```

## Supported Libraries and Their MockSet Objects

Multi-API Mocker provides dedicated pytest fixtures for each supported HTTP client library. While the setup using `MockAPIResponse` is consistent, the returned "mock set" object and its capabilities differ based on how the underlying mocking library operates.

### For `requests` (`requests-mock`)

- **Fixture:** `setup_http_mocks`
- **Returned Object:** `RequestsMockSet`

This fixture integrates with the `requests-mock` library. `requests-mock` intercepts requests and provides mock responses based on registered URIs. The `RequestsMockSet` allows you to access the underlying `requests-mock` `_Matcher` objects via the `get_matcher()` method, which can be used to inspect details of calls *after* they have been made (e.g., `call_count`).

**Example:**
```python
import requests
from . import mocks # Assuming mocks.py with a UserProfile subclass

@pytest.mark.parametrize(
    "setup_http_mocks",
    [([mocks.UserProfile()])],
    indirect=True
)
def test_requests_example(setup_http_mocks):
    response = requests.get("https://api.example.com/user/profile")
    assert response.status_code == 200
    assert response.json()["id"] == "user123"

    # The RequestsMockSet gives you access to the underlying matcher
    matcher = setup_http_mocks.get_matcher("UserProfile")
    assert matcher.call_count == 1
```

### For `httpx` (`pytest-httpx`)

- **Fixture:** `setup_httpx_mocks`
- **Returned Object:** `HTTPXMockSet`

This fixture integrates with `pytest-httpx`. A key difference from `requests-mock` is that `httpx` requests are created just-in-time when they are executed. The `HTTPXMockSet` is designed to help you inspect these requests *after* they have been made via the `get_request()` method, as the request objects are not available until the actual HTTP call occurs.

**Example:**
```python
import httpx
from . import mocks

@pytest.mark.parametrize(
    "setup_httpx_mocks",
    [([mocks.UserProfile()])],
    indirect=True
)
def test_httpx_example(setup_httpx_mocks):
    with httpx.Client() as client:
        response = client.get("https://api.example.com/user/profile")
    
    assert response.status_code == 200
    assert response.json()["id"] == "user123"

    # Use get_request() to inspect the request after it was made
    request = setup_httpx_mocks.get_request("UserProfile")
    assert request.method == "GET"
```

### For `aiohttp` (`aioresponses`)

- **Fixture:** `setup_aiohttp_mocks`
- **Returned Object:** `AIOHTTPMockSet`

This fixture integrates with `aioresponses`. Similar to `httpx`, `aiohttp` requests are asynchronous and handled just-in-time. The `AIOHTTPMockSet` provides a `get_request()` method for inspecting requests *after* they have been executed.

**Example:**
```python
import aiohttp
import pytest
from . import mocks

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "setup_aiohttp_mocks",
    [([mocks.UserProfile()])],
    indirect=True
)
async def test_aiohttp_example(setup_aiohttp_mocks):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.example.com/user/profile") as response:
            assert response.status == 200
            data = await response.json()
            assert data["id"] == "user123"
```

## Advanced Usage

### Simulating Exceptions

You can simulate network errors or other exceptions by passing an `exc` argument to your `MockAPIResponse`.

```python
import requests
from requests.exceptions import ConnectTimeout

@pytest.mark.parametrize(
    "setup_http_mocks", # Or setup_httpx_mocks, setup_aiohttp_mocks
    [([
        mocks.UserProfile(exc=ConnectTimeout("Connection timed out"))
    ])],
    indirect=True
)
def test_with_exception(setup_http_mocks):
    with pytest.raises(ConnectTimeout):
        requests.get("https://api.example.com/user/profile")
```

### Partial JSON Updates

For minor variations in a response, use `partial_json` to update only specific fields of the `default_json` defined in your `MockAPIResponse` (or its subclass).

```python
@pytest.mark.parametrize(
    "setup_http_mocks", # Or setup_httpx_mocks, setup_aiohttp_mocks
    [([
        mocks.UserProfile(partial_json={"name": "John Smith"})
    ])],
    indirect=True
)
def test_with_partial_json(setup_http_mocks):
    response = requests.get("https://api.example.com/user/profile")
    # The rest of the default_json from the UserProfile class remains unchanged
    assert response.json()["name"] == "John Smith"
    assert response.json()["id"] == "user123" 
```

### Advanced Mocking with `MockAPIResponse`

For advanced mocking scenarios, you can use the `MockAPIResponse` class. This class provides additional parameters that map directly to the capabilities of the underlying mocking libraries, giving you more control over the mocked response.

- **`headers`**: A dictionary of response headers.
- **`callback`**: A function that will be called to generate a dynamic response.

#### `aiohttp`

The callback function will receive the URL of the request and any other keyword arguments, and it should return an `aioresponses.CallbackResult` object.

**Example:**
```python
import pytest
from aiohttp import ClientSession
from multi_api_mocker.definitions import MockAPIResponse
from aioresponses import CallbackResult

# Example of a callback function
def dynamic_callback(url, **kwargs):
    # You can add custom logic here to determine the response
    if "error" in kwargs["params"]:
        return CallbackResult(status=500, body="Internal Server Error")
    return CallbackResult(status=200, body="Success")

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "setup_aiohttp_mocks",
    [
        [
            # Mocking with custom headers
            MockAPIResponse(
                url="https://example.com/api/test_headers",
                method="GET",
                json={"message": "Success"},
                status_code=200,
                headers={"X-Custom-Header": "Test-Value"},
            ),
            # Mocking with a dynamic callback
            MockAPIResponse(
                url="https://example.com/api/test_callback",
                method="GET",
                callback=dynamic_callback,
            ),
        ]
    ],
    indirect=True,
)
async def test_advanced_aiohttp_mocking(setup_aiohttp_mocks):
    async with ClientSession() as session:
        # Test custom headers
        async with session.get("https://example.com/api/test_headers") as response:
            assert response.status == 200
            assert await response.json() == {"message": "Success"}
            assert response.headers["X-Custom-Header"] == "Test-Value"

        # Test dynamic callback
        async with session.get("https://example.com/api/test_callback") as response:
            assert response.status == 200
            assert await response.text() == "Success"
```

#### `requests`

The callback function will receive the request object and the context, and it should return a JSON serializable object.

**Example:**
```python
import pytest
import requests
from multi_api_mocker.definitions import MockAPIResponse

# Example of a callback function
def dynamic_callback(request, context):
    context.status_code = 200
    return {"message": "Callback executed"}

@pytest.mark.parametrize(
    "setup_http_mocks",
    [
        [
            MockAPIResponse(
                url="https://example.com/api/test_callback",
                method="GET",
                callback=dynamic_callback,
            )
        ]
    ],
    indirect=True,
)
def test_advanced_http_mocking(setup_http_mocks):
    response = requests.get("https://example.com/api/test_callback")
    assert response.status_code == 200
    assert response.json() == {"message": "Callback executed"}
```

#### `httpx`

The callback function will receive the request object and it should return an `httpx.Response` object.

**Example:**
```python
import pytest
import httpx
from multi_api_mocker.definitions import MockAPIResponse

# Example of a callback function
def dynamic_callback(request):
    return httpx.Response(200, json={"message": "Callback executed"})

@pytest.mark.parametrize(
    "setup_httpx_mocks",
    [
        [
            MockAPIResponse(
                url="https://example.com/api/test_callback",
                method="GET",
                callback=dynamic_callback,
            )
        ]
    ],
    indirect=True,
)
def test_advanced_httpx_mocking(setup_httpx_mocks):
    with httpx.Client() as client:
        response = client.get("https://example.com/api/test_callback")
    assert response.status_code == 200
    assert response.json() == {"message": "Callback executed"}
```


## Deprecation Warnings

The `setup_api_mocks` fixture is deprecated and will be removed in a future release. Please use `setup_http_mocks` for `requests` mocking instead.
