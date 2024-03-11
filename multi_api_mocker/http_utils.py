from collections import defaultdict
from typing import Dict
from typing import List, Union

from requests_mock import Mocker
from requests_mock.adapter import _Matcher

from multi_api_mocker.definitions import MockAPIResponse
from .models import MockConfiguration, ResponseKwargs


class RequestsMockSet:
    """
    A collection class that manages MockAPIResponse objects and integrates with the
    requests_mock fixture. This class provides efficient access and iteration over
    grouped API responses by their endpoint names, simplifying the process of setting
    up and managing multiple mock responses in tests. It also stores and allows access
    to the requests_mock adapter's _Matcher objects associated with each mock response,
    enabling advanced interactions and assertions in tests.

    Parameters:
        api_responses (List[MockAPIResponse]): A list of MockAPIResponse objects, each
                                               representing a specific API response.
        requests_mock (Mocker): The requests_mock fixture instance used for registering
                                the mock API responses.
        matchers (Dict[str, _Matcher]): A dictionary mapping endpoint names to their
                                        respective requests_mock adapter _Matcher
                                        objects.

    Attributes:
        _response_registry (Dict[str, MockAPIResponse]): A dictionary mapping endpoint
                                                         names to their respective
                                                         MockAPIResponse objects.
        requests_mock (Optional[Mocker]): The requests_mock fixture instance.
        matchers (Dict[str, _Matcher]): A dictionary of _Matcher objects, providing
                                        detailed control and inspection capabilities
                                        for the registered mock API responses.

    Methods:
        get_matcher(endpoint_name: str) -> _Matcher: Returns the _Matcher object
                                                     associated with the given
                                                     endpoint name.
    """

    def __init__(
        self,
        api_responses: List[MockAPIResponse],
        requests_mock: Mocker = None,
        matchers: Dict[str, _Matcher] = None,
    ):
        self._response_registry = {
            response.endpoint_name: response for response in api_responses
        }
        self.requests_mock = requests_mock
        self.matchers = matchers or {}

    def __getitem__(self, endpoint_name: str) -> MockAPIResponse:
        return self._response_registry[endpoint_name]

    def __iter__(self):
        return iter(self._response_registry.values())

    def __len__(self):
        return len(self._response_registry)

    def __repr__(self):
        endpoint_names = ", ".join(self._response_registry.keys())
        return f"<{self.__class__.__name__} with endpoints: {endpoint_names}>"

    def get_matcher(self, endpoint_name: str) -> _Matcher:
        return self.matchers.get(endpoint_name)


def group_by_url(
    api_mocks: List[Union[MockAPIResponse, List[MockAPIResponse]]]
) -> List[MockConfiguration]:
    """
    Organizes a list of MockAPIResponse objects by their URL and method, grouping
    them into lists of responses for each endpoint. This grouping is necessary for
    requests-mock when multiple responses for the same endpoint are required, as it
    allows requests-mock to cycle through the responses in order for each subsequent
    call to the same URL.

    Parameters:
        api_mocks (List[Union[MockAPIResponse, List[MockAPIResponse]]]):
            A list of MockAPIResponse objects or lists of MockAPIResponse objects
            representing the expected responses
            for different API calls.

    Returns:
        List[MockConfiguration]:
            A list of MockConfiguration objects where each object
            contains the URL, method, and a list of responses to be
            used by requests-mock to simulate API interactions.
    """

    grouped_mocks = defaultdict(list)
    for mock_definition in api_mocks:
        if isinstance(mock_definition, list):
            for nested_mock_definition in mock_definition:
                if isinstance(nested_mock_definition, MockAPIResponse):
                    add_mock_to_group(grouped_mocks, nested_mock_definition)
                else:
                    raise ValueError(
                        f"Unsupported mock definition type: "
                        f"{type(nested_mock_definition)}"
                    )
        elif isinstance(mock_definition, MockAPIResponse):
            add_mock_to_group(grouped_mocks, mock_definition)
        else:
            raise ValueError(
                f"Unsupported mock definition type: {type(mock_definition)}"
            )

    output = []
    for (url, method), kwargs_list in grouped_mocks.items():
        responses = [kwargs.to_dict() for kwargs in kwargs_list]
        config = MockConfiguration(url=url, method=method.upper(), responses=responses)
        output.append(config)

    return output


def add_mock_to_group(grouped_mocks, mock):
    response_kwargs = ResponseKwargs(
        text=mock.text if not mock.exc else None,
        status_code=mock.status_code if not mock.exc else None,
        json=mock.json if not mock.exc else None,
        exc=mock.exc if mock.exc else None,
    )
    grouped_mocks[(mock.url, mock.method)].append(response_kwargs)
