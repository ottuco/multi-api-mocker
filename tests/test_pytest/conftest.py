try:
    from multi_api_mocker.contrib.pytest_plugin import setup_http_mocks  # noqa: F401
except ImportError:
    pass

try:
    from multi_api_mocker.contrib.pytest_plugin import setup_httpx_mocks  # noqa: F401
except ImportError:
    pass

try:
    from multi_api_mocker.contrib.pytest_plugin import setup_aiohttp_mocks  # noqa: F401
    from multi_api_mocker.contrib.pytest_plugin import aiohttp_available
except ImportError:
    aiohttp_available = False

if aiohttp_available:
    pytest_plugins = "aioresponses"
