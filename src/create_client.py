from typing import Tuple
import js
import os
from pyodide.http import pyfetch
from azure.ai.textanalytics.aio import TextAnalyticsClient
from azure.ai.formrecognizer.aio import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential


async def load_credentials(
    env_endpoint: str = "http://localhost:8000/.env",
) -> Tuple[str, ...]:
    """Try to load keys and endpoints for azure resources.
    First, look for a `.env` file in `http://localhost:8000/.env`
    (this is mostly for rapid development). If anything fails, prompt the
    user for these values.
    """
    try:
        # Might be better to just parse it straight up?
        response = await pyfetch(env_endpoint)
        with open(".env", "wb") as f:
            f.write(await response.bytes())

        # Load keys like this so I can develop fast without hardcoding
        # sensitive information. In the future, these will be prompts.
        from dotenv import load_dotenv

        load_dotenv()
        key = os.getenv("AZ_TEXTANALYTICS_KEY")
        endpoint = os.getenv("AZ_TEXTANALYTICS_ENDPOINT")
    except Exception as e:
        key = js.getElementById("key").value
        endpoint = js.getElementById("endpoint").value
    return (key, endpoint)


# async def create_clients() -> Tuple[TextAnalyticsClient, FormRecognizerClient]:
#     """Create a `TextAnalytics` and a `FormRecognizer` clients in the global Python
#     scope with the `PyodideTransport` transport.
#     """

#     credential = AzureKeyCredential(key)
#     kwargs = {"endpoint": endpoint, "credential": credential, "transport": PyodideTransport()}

#     textanalytics_client = TextAnalyticsClient(
#         endpoint=textanalytics_endpoint,
#         credential=AzureKeyCredential(textanalytics_key),
#         transport=PyodideTransport(),
#     )
#     form_recognizer_client = FormRecognizerClient(
#         endpoint=form_recognizer_endpoint,
#         credential=AzureKeyCredential(form_recognizer_key),
#         transport=PyodideTransport(),
#     )
#     return textanalytics_client, form_recognizer_client
