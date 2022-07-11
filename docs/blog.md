# Running the Azure Python SDK Natively on the Browser

[Pyodide]() is a Python runtime in WebAssembly. It requires no installation nor dependencies. It just
runs Python most browsers. Some of Pyodide's selling points is that is works as a JavaScript alternative.
Pyodide is also a great learning tool as it lets users try Python/Python libraries without needing to worry about the installation (e.g. having different Python executables on a machine).
~~~~
It ahs a few too many keys on the right sight but we take those
test a new keyboard configuration. It a actually doest feel too bad but I would like
the keys to be closer togetger, well not the keys then
My summer intern project was to get the Azure Python SDK to work on Pyodide. This paves the way
to more interactive documentation as well as having a working SDK if Pyodide competing with JavaScript.

The SDK essentially a Pythonic wrapper around HTTP requests to Azure. The issue is that networking on
the browser is completely different than traditional Python networking (think `requests` or
`aiohttp`). Because the browser is made for the everyday person, rather than developers, it includes
a lot more measures to protect users. The browser will do things such as send preflight requests to very
the cross-origin policy of a host, and will also set certain headers. As such, traditional Python network libraries do not work.

The solution is fairly straightforward once one can understand the architecture behind the Azure SDK.
The `core` module is shared by all libraries. It creates a single interface 

