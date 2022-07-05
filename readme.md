# Pyodide Demo

A demo of the Python Azure SDK working [in the browser](https://pyodide.org/en/stable/). 

## Running

To build, run

```bash
npm run build
```

or

```bash
npm run build-dev
```

to create a release or dev build respectively.

## Dependencies

To add a JavaScript dependency, run

```bash
npm install package
```

Python dependencies are a bit more complicated because we have to install them using
`micropip` on the browser. Thus, the local Python environment may be different than
the browser Python environment.

Local dependencies are only used for intellisense and testing.
To install dependencies, in a new virtual environment, install
[poetry](https://python-poetry.org/) and run

```bash
poetry install
```

To add dependencies, run

```bash
poetry add package
```

To add a dependency to the web environment, update the `src/requirements.txt` file. For
test-only dependencies, see the testing docs.

## Azure Resources

Most resources work out of the box, but notable ones fail because of CORS, such as storage.
To set up storage, navigate to your storage client homepage and go to `Resource Sharing (CORS)`.
Under your desired service, create a rule with the following values

| Allowed origins | Allowed methods | Allowed headers | Exposed headers | Max age |
|-----------------|-----------------|-----------------|-----------------|---------|
| \*              | All             | \*              | See below       | 3600    |

For exposed headers, put

> Server,Content-Range,ETag,Last-Modified,Accept-Ranges,x-ms-*

## Testing

Run tests using

```bash
pytest
```

For integration tests, see the testing docs.
