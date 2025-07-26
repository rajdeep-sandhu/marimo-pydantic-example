# Marimo Form Validation using Pydantic (Example/Tutorial)

- This demonstrates validating a pydantic form using a validation callback which validates the data against a Pydantic model.

## Installation

The project is managed using `uv`.

1. **Install [uv](https://github.com/astral-sh/uv):**

    ```sh
    pip install uv
    ```

2. **Install all dependencies from `pyproject.toml`:**

    ```sh
    uv sync
    ```

3. **Activate the virtual environment:**

    ```sh
    # On Unix/macOS:
    source .venv/bin/activate
    # On Windows:
    .venv\Scripts\activate
    ```

4. Run the project

    ```sh
    uv run marimo edit ui_element_validation.py
    ```
