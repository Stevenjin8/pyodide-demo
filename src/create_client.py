from typing import Tuple
import js
import os
from pyodide.http import pyfetch
from azure.ai.textanalytics.aio import TextAnalyticsClient
from azure.ai.formrecognizer.aio import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential


async def load_credentials():
    try:
        response = await pyfetch("http://localhost:8000/.env")
        with open(".env", "wb") as f:
            f.write(await response.bytes())

        # Load keys like this so I can develop fast without hardcoding
        # sensitive information. In the future, these will be prompts.
        from dotenv import load_dotenv

        load_dotenv()
        az_key = os.getenv("AZ_KEY1")
        az_endpoint = os.getenv("AZ_ENDPOINT")
    except Exception as e:
        print(e)
        az_key = js.prompt("Please enter your textanalytics key: ")
        az_endpoint = js.prompt("Please enter your textanalytics endpoint: ")
    return az_key, az_endpoint


async def create_clients() -> Tuple[TextAnalyticsClient, FormRecognizerClient]:
    az_textanalytics_key, az_textanalytics_endpoint = await load_credentials()
    az_form_recognizer_key = os.environ["AZ_FORM_RECOGNIZER_KEY"]
    az_form_recognizer_endpoint = os.environ["AZ_FORM_RECOGNIZER_ENDPOINT"]
    textanalytics_client = TextAnalyticsClient(
        endpoint=az_textanalytics_endpoint,
        credential=AzureKeyCredential(az_textanalytics_key),
        transport=PyodideTransport(),
    )
    formrecognizer_client = FormRecognizerClient(
        endpoint=az_form_recognizer_endpoint,
        credential=AzureKeyCredential(az_form_recognizer_key),
        transport=PyodideTransport(),
    )
    return textanalytics_client, formrecognizer_client


"""
bytes = (await js.document.getElementById("file-upload").files.object_values()[0].stream().getReader().read()).value
type(bytes.to_bytes())
"""
