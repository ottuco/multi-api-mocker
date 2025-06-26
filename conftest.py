from multi_api_mocker.contrib.pytest_plugin import aiohttp_available

if aiohttp_available:
    pytest_plugins = "aioresponses"
