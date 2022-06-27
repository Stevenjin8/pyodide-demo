# Bug in azure storage
import sys
from types import ModuleType

fake_aiohttp = ModuleType("AioHttp")
fake_aiohttp.ClientPayloadError = Exception
sys.modules["aiohttp"] = fake_aiohttp

import asyncio
from typing import List

import js
from js_file import readFileAsync
import micropip

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
async def load_packages() -> None:
    """Loads packages using micropip."""
    promises = [micropip.install(package, keep_going=True) for package in PACKAGES]
    await asyncio.gather(*promises)


async def get_file_bytes(element_id: str) -> bytes:
    """Get the bytes of a file on the website."""
    files = js.document.getElementById(element_id).files.object_values()
    if not len(files):
        raise FileNotFoundError("No file selected.")
    file = files[0]
    return (await readFileAsync(file)).to_bytes()


async def save_files(*_, element_id: str = "file-upload"):
    """Save file to virtual file system."""
    print(element_id)
    input = js.document.getElementById(element_id)
    files = input.files.object_values()
    for file in files:
        with open(file.name, "wb") as f:
            f.write((await readFileAsync(file)).to_bytes())
        js.addToOutput(f"Added {file.name}")
    input.value = ""
