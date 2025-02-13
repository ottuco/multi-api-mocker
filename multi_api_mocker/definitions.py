import inspect
import re
from typing import Any


class MockAPIResponse:
    """
    Represents a mock response for an API endpoint, encapsulating details such as
    the response data, status code, and any associated exceptions. It is designed
    to be subclassed for specific API endpoints, providing a flexible structure
    for defining expected responses in tests.

        Class Attributes:
        url (Union[str, re.Pattern]): Default URL for the API endpoint.
        method (str): Default HTTP method for the endpoint.
        endpoint_name (str): Default identifier for the endpoint.
        default_status_code (int): Default HTTP status code for the response.
        default_json (Any): Default JSON response data.
        default_text (str): Default text response data.
        default_exc (Union[Exception, Type[Exception], None]): Default exception to be
        raised.


    Parameters:
        url (str, optional): The URL of the API endpoint. Defaults to the class-level
                             `url` attribute.
        method (str, optional): The HTTP method. Defaults to the class-level
                                 `method` attribute.
        status_code (int, optional): The HTTP status code of the response. Defaults to
                                     the class-level `status_code` attribute.
        json (Any, optional): The JSON data of the response. Defaults to the
                               class-level `json` attribute or the
                               default JSON data based on the status_code.
        partial_json (dict, optional): Partial dict to update the default_json.
        text (str, optional): The text data of the response. Defaults to the class-level
                              `text` attribute or the default text data based on the
                              status_code.
        exc (Union[Exception, Type[Exception], None], optional): The exception to raise
        when the request is made. Defaults to None.
        **kwargs: Additional keyword arguments for extended configurations or subclass
                  customizations.
    """

    url: str | re.Pattern = None
    method: str = None
    endpoint_name: str = None
    default_status_code: int | None = None
    default_json: Any | None = None
    default_text: str | None = None
    default_exc: Exception | type[Exception] | None = None

    def __init__(
        self,
        url=None,
        method=None,
        status_code=None,
        json=None,
        partial_json=None,
        text=None,
        endpoint_name=None,
        exc=None,
        **kwargs,
    ):
        """
        Initializes a MockAPIResponse object with provided or default values.

        Parameters:
            url (str, optional): The URL of the API endpoint. Defaults to the
                                 class-level `url` attribute.
            method (str, optional): The HTTP method. Defaults to the class-level
                                    `method` attribute.
            status_code (int, optional): The HTTP status code of the response.
                                         Defaults to the class-level `status_code`.
            json (Any, optional): The JSON data of the response. Defaults to the
                                   class-level `json` or default JSON based on
                                   status_code.
            partial_json (dict, optional): Partial dict to update the default_json.
            text (str, optional): The text data of the response. Defaults to the
                                  class-level `text` or default text based on
                                  status_code.
            endpoint_name (str, optional): The name for the API endpoint. Defaults to
                                           the class name.
            exc (Union[Exception, Type[Exception], None], optional): Exception to raise
                for the request. Defaults to None.
            **kwargs: Additional keyword arguments for customizing the response.
        """

        self.url = url or self.__class__.url
        self.method = method or self.__class__.method
        self.endpoint_name = (
            endpoint_name or self.__class__.endpoint_name or self.__class__.__name__
        )
        self._status_code = status_code
        self._partial_json = partial_json
        self._json = json
        self._text = text
        self._exc = exc
        self.kwargs = kwargs

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"url={self.url}, method={self.method}, status_code={self.status_code})"
        )

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.validate_class_attributes()

    @classmethod
    def validate_class_attributes(cls):
        expected_class_attribute_types = {
            "url": (str, re.Pattern),
            "method": (str,),
            "endpoint_name": (str,),
            "default_status_code": (int, type(None)),
            "default_text": (str, type(None)),
        }

        for attr, expected_types in expected_class_attribute_types.items():
            value = getattr(cls, attr, None)
            if not isinstance(value, expected_types) and value is not None:
                expected_type_names = [
                    t.__name__
                    for t in expected_types
                    if t is not type(None)  # noqa: E721
                ]
                if type(None) in expected_types:
                    expected_type_names.append("None")

                type_name = type(value).__name__
                message = (
                    f"The {attr!r} attribute in subclass {cls.__name__!r} "
                    f"must be of type {', '.join(expected_type_names)!r}, "
                    f"got {type_name!r}: {value!r}."
                )
                raise TypeError(message)

        # Separate validation for default_exc because it has different rules
        value = getattr(cls, "default_exc", None)
        if value is not None and not (
            inspect.isclass(value)
            and issubclass(value, Exception)
            or isinstance(value, Exception)
        ):
            raise TypeError(
                f"The 'default_exc' attribute in subclass {cls.__name__!r} "
                f"must be a subclass or instance of Exception or None, "
                f"got {type(value).__name__!r}: {value!r}."
            )

    @property
    def status_code(self):
        return self._status_code or self.__class__.default_status_code

    @property
    def json(self):
        if self._json is not None:
            return self._json
        elif self._partial_json:
            default = self._default_json(self.status_code)
            default.update(self._partial_json)
            return default
        return self._default_json(self.status_code)

    @property
    def text(self):
        if self._text is not None:
            return self._text
        return self._default_text(self.status_code)

    @property
    def exc(self):
        return self._exc or self.__class__.default_exc

    def _default_json(self, status_code):
        return self.default_json.copy() if self.default_json else None

    def _default_text(self, status_code):
        return self.default_text
