import asyncio
from io import StringIO, BytesIO
from typing import List

import js
from js_file import readFileAsync
import micropip

AZ_KEY = None
AZ_ENDPOINT = None

# python-dotenv is useful for development purposes
PACKAGES = ["azure-ai-textanalytics", "python-dotenv", "azure-ai-formrecognizer"]


# `_NATIVE_PRINT`, `_CONSOLE_IO`, and the redifined `print` work to
# override the default behaviour of printing to the devtools console
# rather than the the output of the page. By wrapping wrapping the print
# function for it to write to `_CONSOLE_IO` we can read from it in Javascript
# and manipulate the output how we like.
# See `runPythonConsole` in `index.js`.
_NATIVE_PRINT = print
_CONSOLE_IO = StringIO()


def print(*args, sep=" ", end="\n", file=_CONSOLE_IO, flush=False):
    _NATIVE_PRINT(*args, sep=sep, end=end, file=file, flush=flush)


# Install packages
async def load_packages() -> None:
    """Loads packages using micropip."""
    promises = [micropip.install(package) for package in PACKAGES]
    await asyncio.gather(*promises)


async def get_file_bytes(element_id: str = "file-upload") -> bytes:
    """Get the bytes of a file on the website."""
    files = js.document.getElementById(element_id).files.object_values()
    if not len(files):
        raise FileNotFoundError("No file selected.")
    file = files[0]
    return (await readFileAsync(file)).to_bytes()
