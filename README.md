# Multi-API Mocker: Streamlined API Mocking for pytest


[![PyPI version](https://img.shields.io/pypi/v/multi-api-mocker.svg)](https://pypi.python.org/pypi/multi-api-mocker)


Multi-API Mocker is a Python utility designed to enhance and simplify the process of mocking multiple API calls in pytest tests. Developed as an extension for the [requests_mock](https://github.com/jamielennox/requests-mock)
 package, this tool focuses on improving test readability, maintainability, and efficiency in scenarios requiring multiple API interactions. We extend special thanks to Jamie Lennox for his exceptional work on the requests_mock library, which has been fundamental in the development of this tool. Multi-API Mocker is an ideal solution for developers and testers who regularly work with complex API testing scenarios in pytest.


**Features**:

- **Simplified Mock Management**: Organize and manage multiple API mocks in a clean and intuitive way.
- **Enhanced Readability**: Keep your tests neat and readable by separating mock definitions from test logic.
- **Flexible Response Handling**: Easily define and handle different response scenarios for each API endpoint.
- **Pytest Integration**: Seamlessly integrates with pytest, enhancing its capabilities for API mocking.
- **Reduced Boilerplate**: Less repetitive code, focusing only on the specifics of each test case.
- **Customizable Mocks**: Tailor your mocks to fit various testing scenarios with customizable response parameters.

Multi-API Mocker is a versatile package that seamlessly integrates with both `requests_mock` and `pytest_httpx`, providing a consistent and intuitive interface for mocking API responses in your tests. Whether you're using `requests` or `httpx` for making HTTP requests, Multi-API Mocker has you covered. Switching between the two libraries is a breeze, allowing you to adapt to your project's requirements with minimal effort.

**Installation**:

Multi-API Mocker offers flexible installation options depending on your project's needs. You can choose to install support for either `requests_mock` or `pytest_httpx`, or you can install both for maximum versatility.

To install Multi-API Mocker with `requests_mock` support, run the following command in your terminal:

```bash
pip install multi-api-mocker[http]
```

To install Multi-API Mocker with `pytest_httpx` support, use the following command:

```bash
pip install multi-api-mocker[httpx]
```

If you want to install Multi-API Mocker with support for both `requests_mock` and `pytest_httpx`, you can use the `all` extra:

```bash
pip install multi-api-mocker[all]
```

By specifying the appropriate extra during installation, you can ensure that only the necessary dependencies are installed based on your project's requirements.

Once installed, you can start using Multi-API Mocker in your tests to mock API responses effortlessly. The package provides a set of intuitive fixtures and utilities that work seamlessly with both `requests_mock` and `pytest_httpx`, allowing you to focus on writing comprehensive and maintainable tests.

### Quick Start: Simple Usage

This guide demonstrates how to quickly set up API mocks using `MockAPIResponse` with direct JSON responses in a pytest-parametrized test. This approach is suitable for scenarios where custom subclassing is not necessary.

#### Step 1: Import Necessary Modules

First, import the required modules:

```python
from multi_api_mocker.definitions import MockAPIResponse
import pytest
import requests
```

#### Step 2: Define Your Test with Parametrized Mocks

Now, define your test function and use `pytest.mark.parametrize` to inject the mock responses directly:

```python
@pytest.mark.parametrize(
    "setup_http_mocks",
    [
        (
            [
                MockAPIResponse(
                    url="https://example.com/api/commit",
                    method="POST",
                    json={"message": "Commit successful", "commit_id": "abc123"},
                ),
                MockAPIResponse(
                    url="https://example.com/api/push",
                    method="POST",
                    json={"message": "Push successful", "push_id": "xyz456"},
                ),
            ]
        )
    ],
    indirect=True,
)
def test_commit_and_push(setup_http_mocks):
    # Perform the commit API call
    commit_response = requests.post("https://example.com/api/commit")
    assert commit_response.json() == {
        "message": "Commit successful",
        "commit_id": "abc123",
    }

    # Perform the push API call
    push_response = requests.post("https://example.com/api/push")
    assert push_response.json() == {"message": "Push successful", "push_id": "xyz456"}
```

This setup allows you to define the mock responses directly in the test parameters, offering a straightforward and flexible way to mock multiple API calls within a single test case.

## API Reference

### MockAPIResponse Class

The `MockAPIResponse` class is an essential component of the multi_api_mocker utility, serving as a blueprint for creating mock responses for API endpoints. It is designed to generate configurations that are directly passed to the `requests_mock` initializer, thereby streamlining the process of setting up mock responses in tests. This functionality is especially beneficial in scenarios involving multiple API interactions, as it allows for a structured, reusable approach to defining expected responses.

#### Why Subclass MockAPIResponse?

Subclassing `MockAPIResponse` is recommended for creating customized mock responses tailored to specific API endpoints. This method enhances reusability, reduces redundancy, and offers flexibility in modifying response attributes as needed in different test cases. Subclasses can set default values for common response properties, making it easier to simulate various API behaviors in a consistent manner.

#### Example Subclasses

Here's an example of a subclass representing a commit API endpoint:

```python
class Commit(MockAPIResponse):
    url = "https://example.com/api/commit"
    method = "GET"
    default_status_code = 200
    default_json = {
        "id": "commit102",
        "message": "Initial commit with project structure",
        "author": "dev@example.com",
        "timestamp": "2023-11-08T12:34:56Z",
    }
```

This subclass defines the default URL, HTTP method, status code, and JSON response for a commit endpoint. It can be instantiated directly in tests, or its attributes can be overridden to simulate different scenarios.

For instance, to simulate a scenario where a commit is rejected:

```python
Commit(json={"error": "commit rejected"}, status_code=400)
```

In this example, the `json` and `status_code` parameters override the defaults defined in the `Commit` class, allowing the test to simulate an error response.

#### Class Attributes and Constructor Parameters

1. **url** (`Union[str, re.Pattern]`): The default URL of the API endpoint. It can be a specific string or a regular expression pattern, allowing for versatile matching of endpoints.

2. **method** (`str`): The default HTTP method (GET, POST, etc.) to be used for the mock response. This method will be applied unless explicitly overridden.

3. **endpoint_name** (`str`): A human-readable identifier for the API endpoint. This name facilitates easy tracking and referencing of mock responses in tests.

4. **default_status_code** (`Optional[int]`): Sets the standard HTTP status code for the response, such as 200 for successful requests or 404 for not found errors.

5. **default_json** (`Optional[dict]`): The default JSON data to be returned in the response. It represents the typical response structure expected from the endpoint.

6. **default_text** (`Optional[str]`): Default text to be returned when a non-JSON response is appropriate.

7. **default_exc** (`Optional[Exception]`): An optional exception that, if set, will be raised by default when the endpoint is accessed. Useful for testing error handling.

#### Constructor Parameters

When creating an instance of `MockAPIResponse`, the following parameters can be specified to override the class-level defaults:

1. **url** (`str`, optional): Overrides the default URL for the API endpoint.

2. **method** (`str`, optional): Specifies a different HTTP method for the mock response.

3. **status_code** (`int`, optional): Sets a specific HTTP status code for the instance, different from the class default.

4. **json** (`dict`, optional): Provides JSON data for the response, overriding the default JSON.

5. **partial_json** (`dict`, optional): Allows for partial updates to the default JSON data, useful for minor variations in response structure.

6. **text** (`str`, optional): Overrides the default text response.

7. **endpoint_name** (`str`, optional): Sets a specific endpoint name for the instance.

8. **exc** (`Exception`, optional): Specifies an exception to be raised when the endpoint is accessed.

9. **kwargs**: Additional keyword arguments for extended configurations or customizations.

#### Usage and Behavior

Subclassing and instantiating `MockAPIResponse` provides a powerful and flexible way to define and manage mock responses for API endpoints. These subclasses can be used directly or modified on-the-fly in tests, enabling developers to thoroughly test their applications against a wide range of API response scenarios. This approach keeps test code clean and focused, with mock logic encapsulated within the mock response classes.

### `setup_http_mocks` Pytest Fixture


The `setup_http_mocks` fixture is an integral part of the multi_api_mocker utility, designed to work seamlessly with pytest and the requests_mock package. It provides a convenient way to organize and implement mock API responses in your tests. The fixture accepts a list of `MockAPIResponse` subclass instances, each representing a specific API response. This setup is ideal for tests involving multiple API calls, ensuring a clean separation between test logic and mock definitions.

#### Purpose and Benefits

Using `setup_http_mocks` streamlines the process of configuring mock responses in pytest. It enhances test readability and maintainability by:

- **Separating Mocks from Test Logic**: Keeps your test functions clean and focused on the actual testing logic, avoiding clutter with mock setup details.
- **Reusable Mock Definitions**: Allows you to define mock responses in a centralized way, promoting reusability across different tests.
- **Flexible Response Simulation**: Facilitates the simulation of various API behaviors and scenarios, including error handling and edge cases.

#### How It Works

The fixture integrates with the `requests_mock` pytest fixture, which intercepts HTTP requests and provides mock responses as defined in the `MockAPIResponse` subclasses. When a test function is executed, the fixture:

1. **Collects Mock Configurations**: Gathers the list of `MockAPIResponse` instances provided via pytest's parametrization.
2. **Registers Mock Responses**: Each mock response configuration is registered with the `requests_mock` instance, ensuring the appropriate mock response is returned for each API call in the test.
3. **Yields a `RequestsMockSet` Object**: Returns a `RequestsMockSet` instance, which contains the organized mock responses accessible by their endpoint names.

#### Example Usage

1. **Defining Mock Responses**:

   Create subclasses of `MockAPIResponse` for each API endpoint you need to mock.

   ```python
   class Fork(MockAPIResponse):
       url = "https://example.com/api/fork"
       method = "POST"
       # ... other default attributes ...
   ```

2. **Using the Fixture in Tests**:

   Use `pytest.mark.parametrize` to pass the mock response subclasses to the test function. The `setup_http_mocks` fixture processes these and sets up the necessary mocks.

   ```python
   @pytest.mark.parametrize(
       "setup_http_mocks",
       [([Fork(), Commit(), Push()])],
       indirect=True
   )
   def test_repository_workflow(setup_http_mocks):
       mock_set = setup_http_mocks
       # ... test logic using mock_set ...
   ```

   In this example, the test function `test_repository_workflow` receives a `RequestsMockSet` object containing the mocks for `Fork`, `Commit`, and `Push` endpoints.


### `RequestsMockSet` Class


The `RequestsMockSet` class in the multi_api_mocker utility is a practical and efficient way to manage multiple `MockAPIResponse` objects in your pytest tests. It is designed to store and organize these mock responses, allowing you to easily access and manipulate them as needed.

#### Constructor Parameters

- **api_responses** (`List[MockAPIResponse]`): A list of `MockAPIResponse` objects, each representing a specific mock for an API endpoint.
- **requests_mock** (`Optional[Mocker]`): The `requests_mock` fixture instance, which is automatically passed by the `setup_http_mocks` fixture. It's used for registering the mock API responses.

#### Functionality

`RequestsMockSet` is particularly useful when you are dealing with a series of API calls in a test and need to reference specific mock responses repeatedly. It helps maintain clean and readable test code by centralizing the mock definitions.

#### How to Use `RequestsMockSet`

1. **Initialization**: `RequestsMockSet` is initialized with a list of `MockAPIResponse` instances. These can represent different API calls you intend to mock in your tests.

   ```python
   mock_set = RequestsMockSet([Fork(), Commit(), Push(), ForcePush()])
   print(mock_set)
    # Output: <RequestsMockSet with endpoints: Fork, Commit, Push, ForcePush>
   ```

2. **Accessing Specific Mocks**: To access a specific mock response, use the endpoint name as the key:

   ```python
   fork_response = mock_set["Fork"]
   # Output: Fork(url=https://example.com/api/fork, method=POST, status_code=200)
   ```

3. **Iterating Over Mocks**: You can iterate over all the mocks in the `RequestsMockSet`:

   ```python
   for mock in mock_set:
       # Perform checks or operations on each mock response
   ```

4. **Converting to a List**: To get a list of all mock responses in the `RequestsMockSet`, simply use `list(mock_set)`:

   ```python
   all_mocks = list(mock_set)
   ```

### Usage of `MockAPIResponse` in Different Testing Scenarios

#### Multiple Parametrized Tests with API Calls in Sequence

This approach utilizes multiple parametrized tests to handle different sequences of API calls, demonstrating how to set up and assert behaviors for a series of API interactions under varying conditions. This approach ensures comprehensive coverage of different response scenarios, making it particularly useful when your system is expected to provide a consistent output structure to the client, regardless of the specific API response status.

```python
@pytest.mark.parametrize(
    "setup_http_mocks",
    [
        # Scenario 1: Push fails with a 400 error
        (
            [
                mocks.Fork(),
                mocks.Commit(),
                mocks.Push(status_code=400, json={"error": "Push failed"}),
            ]
        ),
        # Scenario 2: Force push succeeds after a failed push
        (
            [
                mocks.Fork(),
                mocks.Commit(),
                mocks.ForcePush(status_code=400, json={"error": "Force Push failed"}),
            ]
        ),
    ],
    indirect=True,
)
def test_multiple_scenarios(setup_http_mocks):
    mock_set = setup_http_mocks
    # ... Perform API calls and assert responses for each mock ...
```

In both scenarios, the structure of the system's response to the client is expected to remain consistent, whether the underlying API operation succeeds or fails. By grouping error and success scenarios in this way, you can comprehensively test how your system handles different API response conditions while maintaining a consistent output to the client. This method streamlines the testing process, ensuring that all necessary scenarios are covered efficiently.


#### Simulating API Exceptions
This scenario shows how to simulate exceptions in API responses. The test is set up to expect an exception for a specific API call.

```python
@pytest.mark.parametrize(
    "setup_http_mocks",
    [([mocks.Fork(), mocks.Commit(), mocks.Push(exc=RequestException)])],
    indirect=True
)
def test_api_exception_handling(setup_http_mocks):
    mock_set = setup_http_mocks
    # Handling and asserting the exception
    ...
```

#### Partial JSON Updates
Here, the focus is on testing API calls where only a part of the JSON response needs to be altered. This approach avoids the need for creating multiple mock subclasses for minor variations.

```python
@pytest.mark.parametrize(
    "setup_http_mocks",
    [([mocks.Fork(), mocks.Commit(), mocks.Push(partial_json={"id": "partial_id"})])],
    indirect=True
)
def test_api_with_partial_json(setup_http_mocks):
    mock_set = setup_http_mocks

    response = requests.post("https://example.com/api/push")
    expected_json = mock_set["Push"].json
    expected_json["id"] = "partial_id"

    assert response.status_code == 200
    assert response.json() == expected_json
```

### Flexible Parametrization with Indirect Fixture Usage

In this setup, the focus is on demonstrating the flexibility provided by using `indirect=["setup_http_mocks"]` in parametrized tests. This method allows for the inclusion of multiple, varied parameters into the test function. The `user_email` in the given example is just one instance of how diverse parameters can be effectively integrated into tests.
Parametrized tests can be enhanced by combining them with the `setup_http_mocks` fixture using `indirect=["setup_http_mocks"]`. This approach allows for the introduction of additional parameters (`user_email` in this case) that can be varied across different test cases.

```python
@pytest.mark.parametrize(
    "user_email, setup_http_mocks",
    [
        # Example configuration with additional parameter 'user_email'
        ("example@email.com", [mocks.Fork(), mocks.Commit(), mocks.Push()]),
        # Another configuration with a different 'user_email' and modified API response
        (
            "another@email.com",
            [
                mocks.Fork(),
                mocks.Commit(),
                mocks.Push(json={"message": "Custom message"}),
            ],
        ),
    ],
    indirect=["setup_http_mocks"],
)
def test_flexible_parametrization(user_email, setup_http_mocks):
    mock_set = setup_http_mocks
    # Perform API calls and assertions here
```

This structure is highly adaptable and can be utilized for a wide range of scenarios where test configurations need to change dynamically based on different input parameters. The `user_email` parameter is just an illustrative example; the same technique can apply to any number of parameters, such as user roles, request data, or environmental configurations, providing a robust framework for comprehensive and varied testing scenarios.


### Note on using Multi-API Mocker with `pytest_httpx`

When using Multi-API Mocker with `pytest_httpx`, you can use the created definitions interchangeably without any changes to your test code. However, it's important to note that `pytest_httpx` works differently compared to `requests_mock` in terms of when the requests are created.

With `pytest_httpx`, the requests are not created until they are actually executed during the test. To accommodate this behavior, Multi-API Mocker introduces a new `HTTPXMockSet` collection specifically designed for `pytest_httpx`.

The `HTTPXMockSet` collection provides methods and utilities tailored to work with `pytest_httpx`'s deferred request creation. It allows you to retrieve the actual `httpx` requests after they have been executed, enabling you to perform assertions on the request properties.

When using Multi-API Mocker with `pytest_httpx`, you can access the `HTTPXMockSet` collection through the `setup_httpx_mocks` fixture, which is the equivalent of the `setup_http_mocks` fixture used with `requests_mock`.

Keep this difference in mind when working with `pytest_httpx`, and refer to the Multi-API Mocker documentation for specific examples and guidance on using the `HTTPXMockSet` collection effectively in your tests.


### Deprecation Warnings

With the introduction of `httpx` support in Multi-API Mocker, the naming convention for the fixtures has been updated to provide clarity and consistency. The `setup_api_mocks` fixture, which was previously used for mocking API responses with `requests_mock`, has been renamed to `setup_http_mocks`.

However, to ensure backward compatibility and minimize disruption to existing projects, the `setup_api_mocks` fixture is still available and fully functional. When you use `setup_api_mocks` in your tests, it internally points to the `setup_http_mocks` fixture, so your existing code should continue to work without any modifications.

It's important to note that the `setup_api_mocks` fixture is now considered deprecated and will be removed in a future release of Multi-API Mocker. We strongly recommend updating your tests to use the new `setup_http_mocks` fixture to ensure future compatibility and to avoid any potential confusion.

Upgrading to the new fixture is straightforward and only requires renaming the fixture in your test code. Instead of using `setup_api_mocks`, simply replace it with `setup_http_mocks`:

```python
# Old usage (deprecated)
def test_example(setup_api_mocks):
    # Test code using setup_api_mocks

# New usage (recommended)
def test_example(setup_http_mocks):
    # Test code using setup_http_mocks
```

By making this simple change, you'll be aligned with the latest naming convention and ensure that your tests are future-proof.

We recommend gradually updating your tests to use `setup_http_mocks` instead of `setup_api_mocks` to avoid using the deprecated fixture in the long run. This will help keep your test suite up to date and make it easier to maintain.

If you have any questions or need assistance with the upgrade process, please refer to the Multi-API Mocker documentation or reach out to our support channels for guidance.
