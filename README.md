# BKMUS

## Getting Started

Follow these steps to set up and run the analysis:

### 1. Open in VS Code

- Open this folder in [Visual Studio Code](https://code.visualstudio.com/).
- If prompted, install the recommended extensions.

### 2. Set Up Python Environment

- Make sure you have `Python 3.8` or higher installed.
- Create a virtual environment (if not already present):

  ```sh
  python3 -m venv .venv
  ```

- Activate the virtual environment:

  - **macOS/Linux:**

    ```sh
    source .venv/bin/activate
    ```

  - **Windows:**

    ```sh
    .venv\Scripts\activate
    ```

### 3. Install Dependencies

- Install required packages:

  ```sh
  pip install -r requirements.txt
  ```

### 4. Prepare Data

- Place your `DataCollection.xlsx` file in the project root (or update the path in `main.py`).

### 5. Run the Analysis

- In VS Code, open `main.py`.
- Run the script:
  - Press `F5` (if you want to debug), or
  - Open the integrated terminal and run:

    ```sh
    python main.py
    ```

### 6. Deactivate the Virtual Environment

- When you are done, you can deactivate the virtual environment by running:

  ```sh
  deactivate
  ```

This will return your terminal to the system Python environment.
