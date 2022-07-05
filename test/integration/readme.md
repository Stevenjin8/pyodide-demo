# E2E Testing

The mock tests are a good start, but the main place it can fail is the javascript-python
interface, which the mock tests mock.

## Running

For more complete testing, from the root of this project run

```python
python -h http.server <port>
```

Then on your browser, go to `localhost:<port>/test/integration` and the tests will be run in the browser.

## Adding tests

Add tests in `browser_test.py`. I couldn't get `pytest` or `unittest` to cooperate with me,
so I made my own little async testing framework (`async_test.py`). If you are creating new
files to test or new packages, update the `TEST_FILES` and `PACKAGES` variables in
`index.html`.

## Sensitive values

To run the tests, you need a `.env` folder in this directory with your sensitive values.
see `example-env`. You can then access the values as environment variables using `os.getenv`.
