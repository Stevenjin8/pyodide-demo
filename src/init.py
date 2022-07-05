"""Initialize python environment"""
# pyright: reportMissingImports=false
# Bug in azure storage
import sys
from types import ModuleType
from requirements import requirements  # pylint: disable=import-error

import micropip  # pylint: disable=import-error

# Get rid of this after https://github.com/Azure/azure-sdk-for-python/pull/24965
# is pushed into prod.
fake_aiohttp = ModuleType("AioHttp")
fake_aiohttp.ClientPayloadError = Exception
sys.modules["aiohttp"] = fake_aiohttp

# Install packages
# pylint: disable=await-outside-async
await micropip.install(filter(bool, requirements.split("\n")), keep_going=True)  # type: ignore
