# Example of Data Pipeline Application

## 📋 Overview
This project simulates a mini donation data pipeline that:
- Ingests raw donation data in JSON format
- Validates the data using schema rules (via `pandera`)
- Transforms the data with derived features
- Aggregates key metrics for reporting
- Stores outputs in Parquet format

## 🔧 Components

### 1. **Ingestion**
- Reads JSON/CSV/Parquet files using `pandas`
- Validates data types, ranges, and formats
- Saves cleaned data to a staging place

### 2. **Transformation**
- Adds derived features: donation date, hour, tier
- Computes aggregated metrics:
  - Donations per campaign per day
  - Total donations per day
- Saves outputs to the final storage


## Project structure:
There are 2 major layers:
- service layer: service classes (business logic layer)
- process layer: process used as main entries for Python jobs

Folder structure:
```
|-- src
|  |-- constant
|  |-- proess
|  |-- service
|-- tests
|  |-- resources
|  |-- proess
|  |-- service
|-- Pipfile
|-- pyproject.toml
|-- README.md
```

- `src/` directory: root of source code 
- `tests/` directory: root of test source code
- `pyproject.toml`: This file is the heart of modern Python packaging. It defines the project's metadata and build system.
- `README.md`: A good description of your project.

## Important Modules and Libraries
- Interface and Class implementation: Python's **ABC module** is used to achieve this. Link: https://docs.python.org/3.9/library/abc.html
- Schema validation: **Pandera** open source package that provides a flexible and expressive API for performing data validation on dataframe-like objects
- Pandas: is a tool to process and manipulate tabular data. 


## 🛠️ How to Run
```bash
# Ingestion Process
python process/ingestion_process.py --source_data_path <source_data_path> --output_dir_path <output_dir_path> --file_type <file_type>

# Transformation Process
python process/transformation_process.py --source_data_path <source_data_path> --output_dir_path <output_dir_path> --file_type <file_type>
```

## How to Run Test
Pytest is used for testing the application
```bash
# Test the whole app
 pytest

# Example of Test a class or module
pytest tests/service/test_base_service.py
```

Test coverage will be checked during testing. It is configured in the pyproject.toml. Setting can be overwritten if set from command line.
```bash
pytest --cov=src/service 
```
## Virtual Env and Dependency Management
Pipenv is recommended, which is a Python virtualenv management tool that combines pip, virtualenv, and Pipfile into a single unified interface. 
It creates and manages virtual environments for your projects automatically, while also maintaining a Pipfile for package requirements and a Pipfile.lock for deterministic builds.

https://pipenv.pypa.io/en/latest/


## Packing Project
Distributing your Python code in a standardized, efficient format is crucial for sharing your work and ensuring it's easily usable by others. 
The "wheel" format is the modern standard for Python distributions, offering faster installation and greater reliability compared to older formats.

### Installing the Build Tools:

You'll need the build package to create your wheel file. It's best to install it in your project's virtual environment:
```commandline
pip install build
```

### Building the Wheel:

Once you have your pyproject.toml configured and build installed, creating the wheel is a single command executed in the root of your project directory:
```commandline
python -m build
```

This command will create a dist/ directory in your project root. Inside this directory, there will be 2 files.
The .whl file is the packaged project, ready to be installed by pip or uploaded to the Python Package Index (PyPI).
- `my_package-0.1.0-py3-none-any.whl`: This is the wheel file.
- `my-package-0.1.0.tar.gz`: This is a source distribution (sdist).

Note: One needs to manually copy the dependencies from the [packages] section in Pipfile into the dependencies list in the pyproject.toml.
There is no universally adopted, standard tool to automatically convert a Pipfile directly into packaging metadata.
