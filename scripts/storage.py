import asyncio
import os
from turtle import down
from time import time
from uuid import uuid4

from azure.storage.blob.aio import BlobServiceClient, BlobClient
from dotenv import load_dotenv

# from transport import PyodideTransport

load_dotenv(override=True)

KEY = os.environ["AZ_STORAGE_KEY"]
CONNECTION_STRING = os.environ["AZ_STORAGE_CONNECTION_STRING"]


async def main():
    account_client: BlobServiceClient = BlobServiceClient.from_connection_string(
        CONNECTION_STRING,
        # transport=PyodideTransport()
    )
    blob_client = BlobClient(
        account_url=account_client.url,
        container_name="tsjinxuanstorage2",
        blob_name="random",
        credential=account_client.credential,
        max_single_get_size=1,
        max_chunk_get_size=1,
        # transport=PyodideTransport()
    )
    downloader = await blob_client.download_blob()
    start = time()
    async for chunk in downloader.chunks():
        print(chunk)
    print(time() - start)


if __name__ == "__main__":
    asyncio.run(main())
