import re

import httpx
import pytest

from multi_api_mocker.definitions import MockAPIResponse


class TestMockAPIResponse:
    def test_initialization_with_no_kwargs(self):
        mock = MockAPIResponse()
        assert mock.url is None
        assert mock.method is None
        assert mock.endpoint_name == "MockAPIResponse"
        assert mock.status_code is None
        assert mock.json is None
        assert mock.text is None
        assert mock.exc is None

    def test_initialization_with_kwargs(self):
        mock = MockAPIResponse(
            url="https://example.com",
            method="GET",
            status_code=200,
            json={"foo": "bar"},
            text="Hello, world!",
            endpoint_name="MockAPIResponse",
            exc=Exception,
        )
        assert mock.url == "https://example.com"
        assert mock.method == "GET"
        assert mock.endpoint_name == "MockAPIResponse"
        assert mock.status_code == 200
        assert mock.json == {"foo": "bar"}
        assert mock.text == "Hello, world!"
        assert mock.exc is Exception

    def test_subclassing(self):
        class MockAPIResponseSubclass(MockAPIResponse):
            url = "https://example.com"
            method = "GET"
            endpoint_name = "MockAPIResponseSubclass"
            default_status_code = 200
            default_json = {"foo": "bar"}
            default_text = "Hello, world!"
            default_exc = Exception

        mock = MockAPIResponseSubclass()
        assert mock.url == "https://example.com"
        assert mock.method == "GET"
        assert mock.endpoint_name == "MockAPIResponseSubclass"
        assert mock.status_code == 200
        assert mock.json == {"foo": "bar"}
        assert mock.text == "Hello, world!"
        assert mock.exc is Exception

    def test_subclassing_with_exception_instance(self):
        class MockAPIResponseSubclass(MockAPIResponse):
            url = "https://example.com"
            method = "GET"
            endpoint_name = "MockAPIResponseSubclass"
            default_status_code = 200
            default_json = {"foo": "bar"}
            default_text = "Hello, world!"
            default_exc = httpx.TimeoutException(
                message="Timeout error",
                request=httpx.Request("POST", "https://example.com/api/push"),
            )

        mock = MockAPIResponseSubclass()
        assert mock.url == "https://example.com"
        assert mock.method == "GET"
        assert mock.endpoint_name == "MockAPIResponseSubclass"
        assert mock.status_code == 200
        assert mock.json == {"foo": "bar"}
        assert mock.text == "Hello, world!"
        assert isinstance(mock.exc, httpx.TimeoutException)

    def test_subclassing_with_url_as_regex_pattern(self):
        class MockAPIResponseSubclass(MockAPIResponse):
            url = re.compile("https://example.com")
            method = "GET"
            endpoint_name = "MockAPIResponseSubclass"
            default_status_code = 200
            default_json = {"foo": "bar"}
            default_text = "Hello, world!"
            default_exc = Exception

        mock = MockAPIResponseSubclass()
        assert mock.url == re.compile("https://example.com")
        assert mock.method == "GET"
        assert mock.endpoint_name == "MockAPIResponseSubclass"
        assert mock.status_code == 200
        assert mock.json == {"foo": "bar"}
        assert mock.text == "Hello, world!"
        assert mock.exc is Exception

    def test_partial_json(self):
        class MockAPIResponseSubclass(MockAPIResponse):
            url = "https://example.com"
            method = "GET"
            endpoint_name = "MockAPIResponseSubclass"
            default_status_code = 200
            default_json = {"foo": "bar"}
            default_text = "Hello, world!"
            default_exc = Exception

        mock = MockAPIResponseSubclass(partial_json={"bar": "foo"})
        assert mock.json == {"bar": "foo", "foo": "bar"}

    def test_subclassing_with_invalid_url(self):
        with pytest.raises(TypeError) as exc_info:
            # The following line triggers the validation check
            type(
                "MockAPIResponseSubclass",
                (MockAPIResponse,),
                {"url": 1},
            )

        assert (
            str(exc_info.value)
            == "The `url` attribute in subclass `MockAPIResponseSubclass` "
            "must be of type `str, Pattern`, got `int`: `1`."
        )

    @pytest.mark.parametrize(
        "attribute, invalid_value, expected_message",
        [
            (
                "method",
                200,
                "The `method` attribute in subclass `MockAPIResponseSubclass` "
                "must be of type `str`, got `int`: `200`.",
            ),
            (
                "endpoint_name",
                False,
                (
                    "The `endpoint_name` attribute in subclass "
                    "`MockAPIResponseSubclass` must be of type `str`, got `bool`: `False`."  # noqa: E501
                ),
            ),
            (
                "default_status_code",
                "NotAnInt",
                (
                    "The `default_status_code` attribute in subclass `MockAPIResponseSubclass` "  # noqa: E501
                    "must be of type `int, None`, got `str`: `NotAnInt`."
                ),
            ),
            (
                "default_json",
                "NotADict",
                "The `default_json` attribute in subclass `MockAPIResponseSubclass` "
                "must be of type `dict, None`, got `str`: `NotADict`.",
            ),
            (
                "default_text",
                123,
                "The `default_text` attribute in subclass `MockAPIResponseSubclass` "
                "must be of type `str, None`, got `int`: `123`.",
            ),
            (
                "default_exc",
                "NotATypeOrNone",
                "The `default_exc` attribute in subclass `MockAPIResponseSubclass` "
                "must be a subclass or instance of Exception or None, got `str`: "
                "`NotATypeOrNone`.",
            ),
        ],
        ids=[
            "method",
            "endpoint_name",
            "default_status_code",
            "default_json",
            "default_text",
            "default_exc",
        ],
    )
    def test_invalid_class_attribute_definition(
        self, attribute, invalid_value, expected_message
    ):
        # Dynamically create a subclass with an invalid attribute

        with pytest.raises(TypeError) as exc_info:
            # The following line triggers the validation check
            type(
                "MockAPIResponseSubclass",
                (MockAPIResponse,),
                {"url": "https://example.com", attribute: invalid_value},
            )

        assert str(exc_info.value) == expected_message
