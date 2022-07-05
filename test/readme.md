# E2E Testing

The mock tests are a good start, but the main place it can fail is the javascript-python
interface, which the mock tests mock.

## Running

For more complete testing, from the test folder,
run

```python
python -h http.server <port>
```

Then on your browser, go to `localhost:<port>` and the tests will be run in the browser.

## Adding tests

Add tests in `browser_test.py`. If you want to create new test files, create them in
this directory and update the `TEST_FILES` variable in `index.html`. If you are adding
dependencies, remember to also add them to the `PACKAGES` variable.

## Pytest args

To run tests with custom arguments, update the `PYTEST_ARGS` variable in `index.html`.

## Sensitive values

You can access sensitive values by creating a `.env` file:

```
# .env
MY_AZ_SECRET=secret123===
```

You can then access the values as environment variables using `os.getenv`.