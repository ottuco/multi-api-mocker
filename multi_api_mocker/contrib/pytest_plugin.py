import pytest
from requests_mock import Mocker

from ..utils import group_by_url, MockSet


@pytest.fixture(scope="function")
def setup_api_mocks(requests_mock: Mocker, request) -> MockSet:
    """
    A pytest fixture for configuring mock API responses in a test environment.
    It takes subclasses of MockAPIResponse, each representing a unique API call
    configuration. These subclasses facilitate the creation of simple or complex
    response flows, simulating real-world API interactions.

    Parameters:
        requests_mock (Mocker): The pytest requests_mock fixture.
        request: The pytest request object containing parametrized test data.

    Returns:
        MockSet: An instance of MockSet containing the organized MockAPIResponse
                 objects, ready for use in tests.

    The fixture supports multiple test scenarios, allowing for thorough
    testing of varying API response conditions. This is especially useful
    for simulating sequences of API calls like Fork, Commit, and Push
    in a version control system context.

    Example Usage:
        - Single API Call Test:
          @pytest.mark.parametrize("setup_api_mocks", [([Fork()])], indirect=True)

        - Multi-call Sequence Test:
          @pytest.mark.parametrize(
              "setup_api_mocks", [([Fork(), Commit(), Push()])], indirect=True
          )

        - Testing Multiple Scenarios:
        @pytest.mark.parametrize(
            "setup_api_mocks",
            [([Fork(), Commit(), Push()]), ([Fork(), Commit(), ForcePush()])],
            indirect=True
        )


    This fixture converts the list of MockAPIResponse subclasses into MockConfiguration
    instances, registers them with requests_mock, and returns a MockSet object, which
    allows querying each mock by its endpoint name.
    """
    # Convert the incoming parameter to a list of MockConfiguration instances
    api_mocks_configurations = group_by_url(request.param)
    matchers = {}

    # Register each mock configuration with the requests_mock instance
    for api_mock in api_mocks_configurations:
        matcher = requests_mock.register_uri(
            api_mock.method, api_mock.url, api_mock.responses
        )
        matchers[api_mock.url] = matcher

    # Return the requests_mock and the list of MockConfiguration instances
    yield MockSet(request.param, requests_mock, matchers)
