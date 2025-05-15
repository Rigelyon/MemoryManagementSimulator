# Memory Management Simulator

Welcome to Memory Management Simulator. This is a repository used for University project.


## Prerequisites

- Python (v3.12.9 or higher)
- pip
- customtkinter (v5.2.2 or higher)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Rigelyon/MemoryManagementSimulator.git
    cd MemoryManagementSimulator
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv .venv

    # Linux
    source .venv/bin/activate

    # Windows
    .venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Start the app:
    ```bash
    python main.py
    ```

### Build Locally

If you want to create an executable locally:

1. Make sure the environment is installed.
2. Install PyInstaller:
    ```bash
    pip install pyinstaller
    ```
3. Create executable:
    ```bash
    pyinstaller --name "Memory Management Simulator" --windowed --onefile main.py
    ```
4. Executable will be available in the folder `dist/`

## Contributing

Contributions are not accepted as this is a personal project.

## License

This project is licensed under the [MIT License](LICENSE).