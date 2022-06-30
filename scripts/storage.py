import asyncio
import os

from azure.storage.blob import BlobServiceClient, BlobClient
from dotenv import load_dotenv

load_dotenv(override=True)

KEY = os.environ["AZ_STORAGE_KEY"]
ENDPOINT = os.environ["AZ_STORAGE_ENDPOINT"]


async def main():
    account_client = BlobServiceClient(ENDPOINT, KEY)
    blob_client = BlobClient(
        account_url=account_client.url,
        container_name="tsjinxuanstorage2",
        blob_name="large-file",
        credential=account_client.credential,
        max_single_get_size=48 * 1024 * 1024,
        max_chunk_get_size=48 * 1024 * 1024,
        # transport=PyodideTransport()
    )

    downloader = blob_client.download_blob()
    for chunk in downloader.chunks():
        print(chunk)


if __name__ == "__main__":
    asyncio.run(main())
