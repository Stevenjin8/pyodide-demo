# Pyodide Demo

A demo of the Python Azure SDK working in the browser using [PyScript](https://pyscript.net/).

## Running

Just open `index.html` in your browser

## Dependencies

Add them the the `<py-env>` tag in `index.html`.

## Azure Resources

Most resources work out of the box, but notable ones fail because of CORS, such as storage.
To set up storage, navigate to your storage client homepage and go to `Resource Sharing (CORS)`.
Under your desired service, create a rule with the following values

| Allowed origins | Allowed methods | Allowed headers | Exposed headers | Max age |
|-----------------|-----------------|-----------------|-----------------|---------|
| `\*`            | All             | `\*`            | See below       | `3600`  |

For exposed headers, put

> Server,Content-Range,ETag,Last-Modified,Accept-Ranges,x-ms-*
