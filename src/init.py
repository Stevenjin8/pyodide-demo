# pyright: reportMissingImports=false
"""Initialize python environment"""
# Bug in azure storage
import asyncio
import sys
from types import ModuleType

import micropip  # pylint: disable=import-error

fake_aiohttp = ModuleType("AioHttp")
fake_aiohttp.ClientPayloadError = Exception
sys.modules["aiohttp"] = fake_aiohttp


AZ_KEY = None
AZ_ENDPOINT = None

# python-dotenv is useful for development purposes
PACKAGES = [
    "azure-ai-textanalytics",
    "python-dotenv",
    "azure-ai-formrecognizer",
    "azure-storage-blob",
]

# Install packages
# pylint: disable=await-outside-async
promises = [micropip.install(package, keep_going=True) for package in PACKAGES]
await asyncio.gather(*promises)  # type: ignore
