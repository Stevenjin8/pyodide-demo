import initPy from './init.py';
import indexPy from './index.py';
import requirements from './requirements.txt';
import { EXAMPLES } from './examples/examples.js';

const output = document.getElementById('output');

async function main() {
  output.value = 'Initializing...\n';
  // By default, `std{out, err}` go to the console.
  let pyodide = await loadPyodide({
    stdout: (x) => (output.value += x + '\n'),
    stderr: (x) => (output.value += x + '\n'),
  });
  output.value += 'Loading modules...\n';

  await pyodide.registerJsModule('examples', { EXAMPLES });
  await pyodide.registerJsModule('requirements', { requirements });
  await pyodide.loadPackage('micropip');
  await pyodide.runPythonAsync(initPy); // load external modules
  await pyodide.runPythonAsync(indexPy); // DOM interactions

  pyodide.runPython('toggle_inputs(False)'); // Enable inputs
  output.value += 'Ready!\n';
  return pyodide;
}

// Having the promise available in the global scope is
// useful for debugging.
window.pyodideReadyPromise = main();
