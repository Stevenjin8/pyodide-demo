# pyright: reportMissingImports=false
from collections.abc import AsyncIterator

from azure.core.exceptions import ServiceRequestError
from azure.core.pipeline.transport._requests_asyncio import AsyncioRequestsTransport
from azure.core.rest._http_response_impl_async import AsyncHttpResponseImpl
from pyodide.http import pyfetch  # pylint: disable=import-error
from pyodide import JsException  # pylint: disable=import-error
from requests.structures import CaseInsensitiveDict


class PyodideTransport(AsyncioRequestsTransport):
    """Implements a basic HTTP sender using the pyodide javascript fetch api."""

    async def send(self, request, **kwargs):  # type: ignore
        """Send request object according to configuration.

        :param request: The request object to be sent.
        :type request: ~azure.core.pipeline.transport.HttpRequest
        :return: An HTTPResponse object.
        :rtype: PyodideResponseTransport
        """
        endpoint = request.url
        request_headers = dict(request.headers)
        init = {
            "method": request.method,
            "headers": request_headers,
            "body": request.data,
            "files": request.files,
            "verify": kwargs.pop("connection_verify", self.connection_config.verify),
            "cert": kwargs.pop("connection_cert", self.connection_config.cert),
            "allow_redirects": False,
            "keepalive": False,
            **kwargs,
        }

        try:
            response = await pyfetch(endpoint, **init)
        except JsException as error:
            raise ServiceRequestError(error, error=error)

        headers = CaseInsensitiveDict(response.js_response.headers)
        res = PyodideTransportResponse(
            request=request,
            internal_response=response,
            block_size=self.connection_config.data_block_size,
            status_code=response.status,
            reason=response.status_text,
            content_type=headers.get("content-type"),
            headers=headers,
            stream_download_generator=PyodideStreamDownloadGenerator,
        )
        await res.read()
        return res


class PyodideTransportResponse(AsyncHttpResponseImpl):
    async def close(self):
        """This is kinda weird but AsyncHttpResponseImpl assumed that
        the internal response is a `requests.Reponse` object (I think).
        """
        self._is_closed = True

    async def load_body(self):
        if self._content is None:
            self._content = await self.internal_response.bytes()


class PyodideStreamDownloadGenerator(AsyncIterator):
    """Simple stream download generator that returns the contents of
    a request.

    TODO: support paging (?) or like actually doing stream downloading.
    """

    def __init__(self, pipeline, response: PyodideTransportResponse, **__) -> None:
        self.pipeline = pipeline
        self.block_size = response.block_size
        self.request = response.request
        self.response = response
        self.done = False

    def __len__(self):
        return 1

    async def __anext__(self):
        if self.done:
            raise StopAsyncIteration()
        self.done = True
        return await self.response._internal_response.bytes()
