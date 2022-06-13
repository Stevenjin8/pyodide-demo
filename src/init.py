import asyncio
from io import StringIO
from typing import List

import micropip

AZ_KEY = None
AZ_ENDPOINT = None

PACKAGES = ["azure-ai-textanalytics", "python-dotenv"]

# Install packages
async def load_packages():
    """Loads packages using micropip."""
    promises = [micropip.install(package) for package in PACKAGES]
    await asyncio.gather(*promises)
