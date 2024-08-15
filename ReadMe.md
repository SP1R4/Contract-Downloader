# Contract Downloader Script

## Overview

This Python script fetches and saves verified Ethereum smart contract source code from Etherscan. If the contract source code is not verified, it fetches the contract bytecode using Web3. The script is designed to handle multi-file Solidity contracts and offers features such as retry logic, API caching, and improved logging.

## Features

- **Fetch Verified Source Code**: Retrieves verified contract source code from Etherscan.
- **Bytecode Fallback**: Fetches contract bytecode using Web3 if the source code is not verified.
- **Retry Logic**: Automatically retries failed requests up to a specified number of attempts.
- **Caching**: API responses are cached to reduce rate limit issues and improve performance.
- **Logging**: Structured logging with both console and file output.
- **Command-Line Flexibility**: Supports command-line arguments for specifying contract address, output directory, verbosity, retries, and cache settings.
- **Multi-File Solidity Support**: Handles and saves multi-file Solidity contracts in the appropriate folder structure.

## Prerequisites

1. **Python 3.6+**: Ensure Python 3.6 or newer is installed on your system.
2. **Dependencies**: The script uses the following Python packages:
   - `requests`
   - `requests_cache`
   - `web3`
   - `colorama`
   - `tqdm`
   - `python-dotenv`
   - `tenacity` (for retry logic)
   - `json-log-formatter` (for structured logging)

   Install the dependencies using `pip`:

   ```bash
   pip3 install -r requirements.txt
   ```

3. **Infura Project ID**: Obtain an Infura Project ID by creating a project on [Infura](https://infura.io/).
4. **Etherscan API Key**: Get an Etherscan API key by registering on [Etherscan](https://etherscan.io/).

## Setup

1. **Clone the Repository**: Clone the project repository to your local machine:

   ```bash
   git clone https://github.com/SP1R4/Contract-Downloader.git
   cd Contract-Downloader
   ```

2. **Create a `.env` File**: In the project directory, create a `.env` file with the following content:

   ```bash
   ETHERSCAN_API_KEY=your_etherscan_api_key
   INFURA_API_KEY=your_infura_api_key
   ```

   Replace `your_etherscan_api_key` and `your_infura_api_key` with your actual Etherscan and Infura API keys.

3. **Install Dependencies**: Install the required dependencies:

   ```bash
   pip3 install -r requirements.txt
   ```

## Usage

Run the script from the command line with the following syntax:

```bash
python3 main.py <contract_address> [-o OUTPUT_DIR] [-v] [--retry RETRY] [--no-cache]
```

### Arguments

- `<contract_address>`: The Ethereum address of the contract (must be a valid 42-character address starting with '0x').
- `-o, --output-dir`: Optional. Directory to save the contract files (default: `./contracts`).
- `-v, --verbose`: Optional. Increase output verbosity for more detailed logging.
- `--retry`: Optional. Number of retry attempts for API requests (default: 5).
- `--no-cache`: Optional. Disable caching of API responses.

### Example

Fetch and save the source code of a contract:

```bash
python3 main.py 0xContractAddress -o ./contracts -v --retry 3
```

This example fetches the source code of the contract at `0xContractAddress`, saves it in the `./contracts` directory, and retries failed requests up to 3 times.

## Logging

The script logs information to both the console and a file named `contract_downloader.log`. Logs are structured in JSON format and include the following levels:

- `DEBUG`: Detailed logging information (enabled with `-v`).
- `INFO`: General process information.
- `WARNING`: Alerts for potential issues, such as rate limits.
- `ERROR`: Logs errors encountered during execution.

The log file is located in the project directory and provides detailed information about script execution, including timestamps and error messages.

## Directory Structure

When you run the script, the directory structure for multi-file Solidity contracts will be automatically created within the specified output directory. Each contract file will be saved individually in its respective subdirectory if the source code includes multiple files.

Example directory structure:

```
contracts/
└── ContractName/
    ├── File1.sol
    ├── File2.sol
    └── File3.sol
```

## Notes

- **Address Validation**: The script validates Ethereum contract addresses before proceeding.
- **Multi-File Support**: The script supports Solidity contracts that span multiple files and libraries.
- **Retry and Cache**: Built-in retry logic and request caching minimize the impact of network issues and API rate limits.

## License

This script is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve this script. Make sure to adhere to the coding style and ensure all tests pass before submitting a pull request.
