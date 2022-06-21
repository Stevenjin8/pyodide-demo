import asyncio
from io import StringIO, BytesIO
from typing import List

import js
from js_file import readFileAsync
import micropip

AZ_KEY = None
AZ_ENDPOINT = None

PACKAGES = ["azure-ai-textanalytics", "python-dotenv", "azure-ai-formrecognizer"]

# Install packages
async def load_packages() -> None:
    """Loads packages using micropip."""
    promises = [micropip.install(package) for package in PACKAGES]
    await asyncio.gather(*promises)


async def get_file_bytes(element_id: str = "file-upload") -> bytes:
    reader = js.FileReader.new()
    file = js.document.getElementById(element_id).files.object_values()[0]
    return (await readFileAsync(file)).to_bytes()
