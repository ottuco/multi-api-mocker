try:
    from multi_api_mocker.contrib.pytest_plugin import setup_http_mocks  # noqa: F401
except ImportError:
    pass

try:
    from multi_api_mocker.contrib.pytest_plugin import setup_httpx_mocks  # noqa: F401
except ImportError:
    pass

try:
    from multi_api_mocker.contrib.pytest_plugin import (
        setup_aiohttp_mocks,
        aiohttp_available,
    )  # noqa: F401
except ImportError:
    aiohttp_available = False

if aiohttp_available:
    pytest_plugins = "aioresponses"
