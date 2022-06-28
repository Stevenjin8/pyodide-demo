import initPy from './init.py';
import transportPy from './transport.py';
import indexPy from './index.py';

const output = document.getElementById('output');

async function main() {
  output.value = 'Initializing...\n';
  // By default, `std{out, err}` go to the console.
  let pyodide = await loadPyodide({
    stdout: (x) => (output.value += x + '\n'),
    stderr: (x) => (output.value += x + '\n'),
  });
  output.value += 'Loading modules...\n';

  await pyodide.loadPackage('micropip');
  await pyodide.runPythonAsync(initPy); // load external modules
  await pyodide.runPythonAsync(transportPy); // pyodide transports
  await pyodide.runPythonAsync(indexPy); // DOM interactions

  pyodide.runPython('toggle_inputs(False)'); // Enable inputs
  output.value += 'Ready!\n';
  return pyodide;
}

// Having the promise available in the global scope is
// useful for debugging.
window.pyodideReadyPromise = main();
