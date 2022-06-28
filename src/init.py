"""Initialize python environment"""
# pyright: reportMissingImports=false
# Bug in azure storage
import sys
from types import ModuleType

import micropip  # pylint: disable=import-error

# Get rid of this after https://github.com/Azure/azure-sdk-for-python/pull/24965
# is pushed into prod.
fake_aiohttp = ModuleType("AioHttp")
fake_aiohttp.ClientPayloadError = Exception
sys.modules["aiohttp"] = fake_aiohttp

PACKAGES = [
    "azure-ai-textanalytics",
    "azure-ai-formrecognizer",
    "azure-storage-blob",
]

# Install packages
# pylint: disable=await-outside-async
await micropip.install(PACKAGES, keep_going=True)  # type: ignore
