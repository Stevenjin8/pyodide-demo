# pylint: disable=await-outside-async, undefined-variable, consider-using-f-string
from azure.storage.blob.aio import BlobClient

blob_client = BlobClient(
    account_url=client.url,  # type: ignore
    container_name="<your container name>",
    blob_name="<your blob name>",
    credential=client.credential,  # type: ignore
    max_single_get_size=1,
    max_chunk_get_size=1,
    transport=PyodideTransport(),  # type: ignore
)

downloader = await blob_client.download_blob()  # type: ignore
async for chunk in downloader.chunks():  # type: ignore
    print(chunk)
