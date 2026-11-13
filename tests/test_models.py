from multi_api_mocker.models import ResponseKwargs, MockConfiguration


def test_response_kwargs_to_dict():
    kwargs = ResponseKwargs(
        text="test",
        status_code=200,
        json={"foo": "bar"},
        exc=Exception,
        headers={"X-Custom-Header": "Test-Value"},
    )
    assert kwargs.to_dict() == {
        "text": "test",
        "status_code": 200,
        "json": {"foo": "bar"},
        "exc": Exception,
        "headers": {"X-Custom-Header": "Test-Value"},
    }


def test_response_kwargs_to_dict_with_none_values():
    kwargs = ResponseKwargs(
        text="test",
        status_code=200,
    )
    assert kwargs.to_dict() == {
        "text": "test",
        "status_code": 200,
    }


def test_mock_configuration():
    config = MockConfiguration(
        url="https://example.com",
        method="GET",
        responses=[{"json": {"foo": "bar"}}],
    )
    assert config.url == "https://example.com"
    assert config.method == "GET"
    assert config.responses == [{"json": {"foo": "bar"}}]
