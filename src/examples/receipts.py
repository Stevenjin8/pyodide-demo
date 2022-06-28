# pylint: disable=await-outside-async, undefined-variable
with open("receipt.jpeg", "rb") as f:
    data = f.read()
poller = await client.begin_recognize_receipts(data)  # type: ignore
result = (await poller.result())[0]  # type: ignore
for k, v in result.fields.items():
    print(k, ":", v.value_data.text if v.value_data else "-")
