import js
import os
from pyodide.http import pyfetch
from azure.ai.textanalytics.aio import TextAnalyticsClient
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


async def create_client():
    az_key, az_endpoint = await load_credentials()
    print(az_key, az_endpoint)
    return TextAnalyticsClient(
        endpoint=az_endpoint,
        credential=AzureKeyCredential(az_key),
        transport=PyodideTransport(),
    )

"""
bytes = (await js.document.getElementById("file-upload").files.object_values()[0].stream().getReader().read()).value
type(bytes.to_bytes())
"""
