# Python Instagram Bot

This project contains a Python script for automating Instagram interactions using the Selenium library.

## Features

- Login to an Instagram account.
- Like photos based on specified hashtags.

## Requirements

To run this bot, you will need:

- Python 3
- Selenium library:
  ```bash
  pip install selenium
  ```
- Firefox browser
- GeckoDriver: Ensure that GeckoDriver is installed and in your system's PATH. It must be compatible with your Firefox browser version. Alternatively, you can modify the script to use a different browser and its corresponding WebDriver.

## Usage

1.  **Configure Credentials:**
    Open `main.py` and update the `username` and `password` variables with your Instagram credentials:
    ```python
    username = "YOUR_USERNAME"
    password = "YOUR_PASSWORD"
    ```
    **Note:** Hardcoding credentials directly in the script is not recommended for security reasons, especially if you plan to share or version control this code. Consider using environment variables or a configuration file for better security.

2.  **Run the Bot:**
    Execute the script from your terminal:
    ```bash
    python main.py
    ```

## Running Tests

Unit tests have been added for the `InstagramBot` class to ensure its functionality.

To run the tests, use the following command in your terminal:
```bash
python -m unittest test_main.py
```

**Note:** Before running the tests, you might need to install the necessary dependencies. The primary dependency for these tests is `selenium`. You can install it using pip:
```bash
pip install selenium
```