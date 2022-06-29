"""Tests that mock the browser layer."""
import functools
from azure.ai.textanalytics.aio import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import sys
from unittest import mock

import pytest

MOCK_PYODIDE_HTTP = mock.Mock()
MOCK_PYODIDE_HTTP.pyfetch = mock.AsyncMock(return_value="hello")
sys.modules["pyodide.http"] = MOCK_PYODIDE_HTTP

import transport

PLACEHOLDER_ENDPOINT = "https://my-resource-group.cognitiveservices.azure.com/"
PLACEHOLDER_KEY = "abcdefghijklmnopqrstuvwxyz1234567890"


def create_mock_response(
    body: bytes, headers: dict, status: int, status_text: str
) -> mock.Mock:
    mock_response = mock.Mock()
    mock_response.body = body
    mock_response.js_response.headers = headers
    mock_response.status = status
    mock_response.status_text = status_text
    mock_response.bytes = mock.AsyncMock(return_value=body)
    return mock_response


def reset_mock_pyfetch(func: callable) -> callable:
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        MOCK_PYODIDE_HTTP.pyfetch.reset_mock()
        return func(*args, **kwargs)

    return wrapped


@reset_mock_pyfetch
@pytest.mark.asyncio
async def test_sentiment_analysis_success():
    """Tests that a successful sentiment analysis call is processed correctly."""
    body = {
        "documents": [
            {
                "id": "0",
                "sentiment": "positive",
                "confidenceScores": {
                    "positive": 0.99,
                    "neutral": 0.0,
                    "negative": 0.00,
                },
                "sentences": [
                    {
                        "sentiment": "positive",
                        "confidenceScores": {
                            "positive": 0.92,
                            "neutral": 0.0,
                            "negative": 0.07,
                        },
                        "offset": 0,
                        "length": 67,
                        "text": "The food and service were unacceptable, but the concierge were nice",
                    }
                ],
                "warnings": [],
            }
        ],
        "errors": [],
        "modelVersion": "2021-10-01",
    }
    headers = {
        "access-control-allow-origin": "*",
        "access-control-expose-headers": "Operation-Location,Location,Apim-Request-Id",
        "content-type": "application/json; charset=utf-8",
        "date": "Wed, 29 Jun 2022 16:44:23 GMT",
    }
    MOCK_PYODIDE_HTTP.pyfetch.return_value = create_mock_response(
        body=body, headers=headers, status=200, status_text="OK"
    )
    documents = ["The concierge were nice"]
    client = TextAnalyticsClient(
        credential=AzureKeyCredential(PLACEHOLDER_KEY),
        endpoint=PLACEHOLDER_ENDPOINT,
        transport=transport.PyodideTransport(),
    )
    result = await client.analyze_sentiment(documents, show_opinion_mining=False)
    assert len(result) == 1
    transport.pyfetch.assert_called_once()
