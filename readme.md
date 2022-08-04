# Pyodide Demo

A demo of the Python Azure SDK working in the browser using [PyScript](https://pyscript.net/).

## Running

Just open `index.html` in your browser

## Dependencies

Add them the the `<py-env>` tag in `index.html`. Note that this demo is using
a branch of `azure-core` hosted in Azure blob storage because Pyodide-related classes are not in `main`.

## Azure Resources

Most resources work out of the box, but notable ones fail because of CORS, such as storage.
To set up storage, navigate to your storage client homepage and go to `Resource Sharing (CORS)`.
Under your desired service, create a rule with the following values

| Allowed origins | Allowed methods | Allowed headers | Exposed headers | Max age |
|-----------------|-----------------|-----------------|-----------------|---------|
| `\*`            | All             | `\*`            | See below       | `3600`  |

For exposed headers, put

> Server,Content-Range,ETag,Last-Modified,Accept-Ranges,x-ms-*

> **IMPORTANT**: If you want to host a custom wheel of `azure-core` in Azure blob storage and access it via Pyodide, you **must** also add the above CORS rule to the corresponding storage account.