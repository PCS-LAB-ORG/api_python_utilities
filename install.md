Creating a Python utility library involves structuring your code as a package, making it installable, and importing it into other projects. This process uses standard tools like venv and pip. 
PyPI · The Python Package Index
PyPI · The Python Package Index
 +4
Step 1: Create the Library Structure
First, create a project directory and a virtual environment to manage dependencies in isolation. 
Medium
Medium
bash
mkdir my_utility_library
cd my_utility_library
python3 -m venv venv
source venv/bin/activate  # On Windows use '.\venv\Scripts\activate'
pip install setuptools wheel build twine # Install packaging tools
Next, structure your project with a source directory (the actual package), an __init__.py file (which marks the directory as a Python package), and a pyproject.toml file to configure metadata. 
Python.org
Python.org
 +1
my_utility_library/
├── src/
│   └── myutils/
│       ├── __init__.py
│       └── helpers.py
├── pyproject.toml
└── README.md
In src/myutils/helpers.py, add your utility functions:
python
# src/myutils/helpers.py
def say_hello(name):
    return f"Hello, {name}!"

def multiply(a, b):
    return a * b
In src/myutils/__init__.py, you can leave it empty or import functions to make them directly accessible:
python
# src/myutils/__init__.py
from .helpers import say_hello, multiply
In pyproject.toml, configure your package metadata and build system using the Python Packaging User Guide: 
toml
# pyproject.toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "myutils"
version = "0.1.0"
author = "Your Name"
description = "A utility library example"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT License"}
dependencies = [
    # list any dependencies here, e.g., "requests",
]
Step 2: Install the Library Locally
You can install your library locally in editable mode using pip install -e . from the project's root directory (my_utility_library/). This is best for development as changes in the source code are immediately reflected without needing to reinstall. 
Medium
Medium
 +4
bash
# From the root directory of your project (my_utility_library/)
pip install -e .
Alternatively, to simulate how a user would install it, you can build a distribution archive (wheel file) and install that: 
Build the package:
bash
python3 -m build
This creates a dist/ directory with a .whl file.
Install the wheel file:
bash
pip install dist/*.whl
 
Medium
Medium
 +1
Step 3: Use the Utility Library 
Once installed, you can use your utility library in any other Python script or project (within the same virtual environment if applicable). 
Create a new Python file outside of your library's source directory (e.g., test_script.py in the root directory my_utility_library/):
python
# test_script.py
from myutils import say_hello, multiply

message = say_hello("World")
result = multiply(5, 3)

print(message)
print(f"5 * 3 = {result}")
Run the script:
bash
python3 test_script.py
This should output:
Hello, World!
5 * 3 = 15
Step 4: Share Your Library (Optional)
To share your library globally so others can install it with pip install myutils, you need to upload it to the Python Package Index (PyPI) using a tool like twine. The Python Packaging User Guide provides a detailed tutorial for this process. 
Python.org
Python.org
 +3