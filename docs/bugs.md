# Bugs

A record of bugs or weird things I see while working on this project.

## `BlobServiceClient` Credentials

Overall, I found the Blob Storage DX to be quite different than that of Text Analytics
or Form Recognizer:

1. The docs use a connection string rather than a url and credential
2. When instantiating a client with a url and credential:
   1. The credentials field will take the key as a string but not an `AzureKeyCredential` object.
   2. I could not find the account url on the portal and had to reverse-engineer it by creating a client using the connection string and then inspecting the `url` field.

## Hard `requests` dependency

In the `setup.py` of `azure-core`, there is a hard dependency on `requests`.

## Hard networking dependencies in Blob Storage library

See #25084 and #25017 in the Python SDK repo. TLDR: the storage library is importing
`requests` and `aiohttp` exceptions, when `azure.core` should be handling those
exceptions.


## Testing

I really wanted to use `pytest` for my integration tests, and synchronous testing
worked really well, but using `pytest-asyncio` failed because it kept trying to close
the event loop which threw a `NotImplementedError`. To see for yourself, run

```bash
python -m http.server
```

from the root of this repository and open `http://localhost:8000/docs/html/testing.html`.

## Core imports with strings

Because of the out of place `aiohttp` import in storage (#2508 on the Python SDK repo),
I needed to import my library as a fixture so I could patch `sys.modules` to include
a fake `aiohttp` (see the [test file](https://github.com/Azure/azure-sdk-for-python/blob/67efe58e192fb873a97856b75b13d68ab099a6d0/sdk/core/azure-core/tests/test_pyodide_transport.py#L26)).

It might seem weird that I am have 

```python
import azure.core.pipeline.transport._pyodide

yield azure.core.pipeline.transport._pyodide
```

instead of

```python
from azure.core.pipeline.transport import _pyodide

yield _pyodide
```

but in the latter case, I ended up with `_pyodide = 'pyodide'`. Yes, you read that
right. It turned into a string.

## Async functions not awaiting properly

This one was a head scratcher. See `html/async-bug-example` for more details.