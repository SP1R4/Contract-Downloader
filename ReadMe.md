# Contract Downloader Script

## Overview

This Python script fetches and saves verified Ethereum smart contract source code from Etherscan. If the contract source code is not verified, it fetches the contract bytecode using Web3.

## Features

- Fetches verified contract source code from Etherscan.
- Retrieves contract bytecode if the source code is not verified.
- Saves the contract source code or bytecode to a specified directory.
- Caches API requests to minimize rate limit issues.
- Supports command-line arguments for flexibility.

## Prerequisites

1. **Python 3.6+**: Ensure Python 3.6 or newer is installed on your system.
2. **Dependencies**: The script uses the following Python packages:
   - `requests`
   - `requests_cache`
   - `web3`
   - `colorama`
   - `tqdm`
   - `python-dotenv`

   Install the dependencies using `pip`:

   ```bash
   pip3 install requests requests_cache web3 colorama tqdm python-dotenv
   ```

3. **Infura Project ID**: Obtain an Infura Project ID by creating a project on [Infura](https://infura.io/).

4. **Etherscan API Key**: Get an Etherscan API key by registering on [Etherscan](https://etherscan.io/).

## Setup

1. **Create a `.env` File**: In the project directory, create a `.env` file with the following content:

   ```
   ETHERSCAN_API_KEY=your_etherscan_api_key
   ```

   Replace `your_etherscan_api_key` with your actual Etherscan API key.

2. **Infura Project ID**: Update the Infura Project ID in the script:

   ```python
   web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'))
   ```

   Replace `YOUR_INFURA_PROJECT_ID` with your actual Infura Project ID.

## Usage

Run the script from the command line with the following syntax:

```bash
python3 GetContractCode.py <contract_address> [-o OUTPUT_DIR] [-v]
```

### Arguments

- `<contract_address>`: The Ethereum address of the contract (must be 42 characters long, starting with '0x').
- `-o, --output-dir`: Optional. Directory to save the contract files (default: current directory).
- `-v, --verbose`: Optional. Increase output verbosity (show more logging information).

### Example

Fetch and save the source code of a contract:

```bash
python3 GetContractCode.py 0xContractAddress -o ./contracts -v
```

## Logging

The script logs information to both the console and a file named `contract_downloader.log`. Log levels include:

- `INFO`: General information about the process.
- `WARNING`: Warnings about potential issues (e.g., rate limits).
- `ERROR`: Errors encountered during execution.

## Notes

- Ensure that the contract address provided is valid.
- The script handles rate limits and network errors gracefully.
- Multi-file Solidity contracts are supported and saved individually.

## License

This script is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to submit issues or pull requests to improve this script.

