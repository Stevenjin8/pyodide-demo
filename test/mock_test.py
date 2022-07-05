"""Tests that mock the browser layer."""
import functools
import json
import sys
from unittest import mock

import pytest
from azure.ai.textanalytics.aio import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.storage.blob._shared.authentication import SharedKeyCredentialPolicy
from azure.storage.blob.aio import BlobClient, BlobServiceClient

# Set up modules
MOCK_PYODIDE_HTTP = mock.Mock()
MOCK_PYODIDE_HTTP.pyfetch = mock.AsyncMock()
sys.modules["pyodide.http"] = MOCK_PYODIDE_HTTP

MOCK_PYODIDE_MODULE = mock.Mock()
MOCK_PYODIDE_MODULE.JsException = Exception
sys.modules["pyodide"] = MOCK_PYODIDE_MODULE
# patch dict
import transport

PLACEHOLDER_ENDPOINT = "https://my-resource-group.cognitiveservices.azure.com/"
PLACEHOLDER_KEY = "abcdefghijklmnopqrstuvwxyz1234567890"


def create_mock_response(
    body: bytes, headers: dict, status: int, status_text: str
) -> mock.Mock:
    """Create a mock response object that mimics `pyodide.http.FetchResponse`"""
    mock_response = mock.Mock()
    if isinstance(body, str):
        body = bytes(body, encoding="utf-8")
    mock_response.body = body
    mock_response.js_response.headers = headers
    mock_response.status = status
    mock_response.status_text = status_text
    mock_response.bytes = mock.AsyncMock(return_value=body)
    return mock_response


def reset_mock_pyfetch(func: callable) -> callable:
    """Decorator that resets our mock `pyfetch`."""

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        MOCK_PYODIDE_HTTP.pyfetch.reset_mock()
        return func(*args, **kwargs)

    return wrapped


@reset_mock_pyfetch
@pytest.mark.asyncio
async def test_sentiment_analysis_success():
    """Tests that a successful sentiment analysis call is processed correctly."""

    with open("test/data/successful-sentiment-analysis.json", "rb") as f:
        body = f.read()
    parsed_body = json.loads(body)

    # Create mock response
    headers = {
        "access-control-allow-origin": "*",
        "access-control-expose-headers": "Operation-Location,Location,Apim-Request-Id",
        "content-type": "application/json; charset=utf-8",
        "date": "Wed, 29 Jun 2022 16:44:23 GMT",
    }
    MOCK_PYODIDE_HTTP.pyfetch.return_value = create_mock_response(
        body=body, headers=headers, status=200, status_text="OK"
    )
    # make the requests
    documents = ["The concierge were nice"]
    client = TextAnalyticsClient(
        credential=AzureKeyCredential(PLACEHOLDER_KEY),
        endpoint=PLACEHOLDER_ENDPOINT,
        transport=transport.PyodideTransport(),
    )
    results = await client.analyze_sentiment(documents, show_opinion_mining=False)

    # check that values match
    expected_document = parsed_body["documents"][0]
    assert len(results) == 1
    result = results[0]
    assert len(result.warnings) == 0
    assert not result.is_error
    assert result.sentiment == expected_document["sentiment"]
    assert (
        result.confidence_scores.positive
        == expected_document["confidenceScores"]["positive"]
    )
    assert (
        result.confidence_scores.neutral
        == expected_document["confidenceScores"]["neutral"]
    )
    assert (
        result.confidence_scores.negative
        == expected_document["confidenceScores"]["negative"]
    )

    assert len(result.sentences) == 1
    sentence = result.sentences[0]
    expected_sentence = expected_document["sentences"][0]
    assert sentence.sentiment == expected_document["sentiment"]
    assert (
        sentence.confidence_scores.positive
        == expected_sentence["confidenceScores"]["positive"]
    )
    assert (
        sentence.confidence_scores.neutral
        == expected_sentence["confidenceScores"]["neutral"]
    )
    assert (
        sentence.confidence_scores.negative
        == expected_sentence["confidenceScores"]["negative"]
    )
    assert sentence.offset == expected_sentence["offset"]
    assert sentence.length == expected_sentence["length"]
    assert sentence.text == expected_sentence["text"]

    # check the call args and kwargs
    transport.pyfetch.assert_called_once()
    call_args = transport.pyfetch.call_args.args
    assert len(call_args) == 1
    assert call_args[0].startswith(PLACEHOLDER_ENDPOINT)
    call_kwargs = transport.pyfetch.call_args.kwargs
    auth_header = call_kwargs["headers"]["Ocp-Apim-Subscription-Key"]
    assert auth_header == PLACEHOLDER_KEY


@reset_mock_pyfetch
@pytest.mark.asyncio
@mock.patch(
    "azure.storage.blob._shared.authentication.SharedKeyCredentialPolicy._add_authorization_header",
)
async def test_successful_blob_storage(*_):
    """Test that we can get stream from blob storage."""

    with open("./test/data/successful-blob-download.json", "r") as file_:
        expected_responses = json.load(file_)

    client = BlobServiceClient(
        PLACEHOLDER_ENDPOINT, SharedKeyCredentialPolicy("a", "b")
    )
    blob_client = BlobClient(
        account_url=client.url,
        container_name="tsjinxuanstorage2",
        blob_name="random",
        credential=client.credential,
        max_single_get_size=1,
        max_chunk_get_size=1,
        transport=transport.PyodideTransport(),
    )

    kwargs = expected_responses["shared"]
    kwargs.update(expected_responses["responses"][0])
    kwargs["headers"].update(expected_responses["shared"]["headers"])
    MOCK_PYODIDE_HTTP.pyfetch.return_value = create_mock_response(**kwargs)
    downloader = await blob_client.download_blob()
    iter_ = downloader.chunks()
    i = 1
    chunk = await iter_.__anext__()  # pylint: disable=unnecessary-dunder-call
    while True:
        try:
            chunk = await iter_.__anext__()  # pylint: disable=unnecessary-dunder-call
            assert chunk == bytes(
                kwargs["body"], encoding="utf-8"
            )  # there must be a better way to do this
            kwargs = expected_responses["shared"]
            kwargs.update(expected_responses["responses"][i])
            kwargs["headers"].update(expected_responses["shared"]["headers"])
            MOCK_PYODIDE_HTTP.pyfetch.return_value = create_mock_response(**kwargs)
            i += 1
        except StopAsyncIteration:
            break

    assert MOCK_PYODIDE_HTTP.pyfetch.call_count == len(expected_responses["responses"])


@pytest.mark.asyncio
async def test_js_exception():
    """Test that exceptions are being caught correctly."""
    MOCK_PYODIDE_HTTP.pyfetch.side_effect = MOCK_PYODIDE_MODULE.JsException()
    documents = ["The concierge were nice"]
    client = TextAnalyticsClient(
        credential=AzureKeyCredential(PLACEHOLDER_KEY),
        endpoint=PLACEHOLDER_ENDPOINT,
        transport=transport.PyodideTransport(),
    )
    with pytest.raises(HttpResponseError):
        await client.analyze_sentiment(documents, show_opinion_mining=False)
