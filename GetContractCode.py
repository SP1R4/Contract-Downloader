import os
import logging
import requests
import argparse
from colorama import Fore, Style, init
from tqdm import tqdm
from web3 import Web3
import requests_cache
from dotenv import load_dotenv

# Initialize colorama for colored output
init(autoreset=True)

# Initialize cache for API requests (5 minutes caching)
requests_cache.install_cache('etherscan_cache', expire_after=300)

# Load environment variables from a .env file
load_dotenv()

# Get Etherscan API key from environment variables
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("contract_downloader.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# Validate API key
if not ETHERSCAN_API_KEY:
    raise ValueError(f"{Fore.RED}Etherscan API key not found in environment variables. Please set ETHERSCAN_API_KEY.")


def setup_argparse():
    """
    Sets up command-line argument parsing using argparse.
    Returns the parsed arguments including the contract address, output directory, and verbosity flag.
    """
    parser = argparse.ArgumentParser(
        description="Fetch and save verified contract source code from Etherscan."
    )

    parser.add_argument(
        "contract_address",
        type=str,
        help="The Ethereum address of the contract (must be 42 characters, starting with '0x')."
    )

    parser.add_argument(
        "-o", "--output-dir",
        default=".",
        type=str,
        help="Directory to save the contract files (default: current directory)."
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Increase output verbosity (show more logging information)."
    )

    return parser.parse_args()


def fetch_contract_source_code(contract_address):
    """
    Fetches the verified contract source code from Etherscan.
    Args:
        contract_address (str): The Ethereum contract address.
    Returns:
        dict: Contract source code data from Etherscan if available, otherwise None.
    """
    url = f"https://api.etherscan.io/api"
    params = {
        "module": "contract",
        "action": "getsourcecode",
        "address": contract_address,
        "apikey": ETHERSCAN_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data["status"] != "1":
            if data["message"] == "Max rate limit reached":
                logger.warning(f"{Fore.YELLOW}Rate limit reached. Please wait and try again later.")
            else:
                logger.error(f"{Fore.RED}Error fetching contract source code: {data['message']}")
            return None

        return data["result"]

    except requests.RequestException as e:
        logger.error(f"{Fore.RED}Network error: {e}")
        return None


def fetch_contract_bytecode(web3, contract_address):
    """
    Fetches the bytecode of a contract using Web3 if the source code is not verified on Etherscan.
    Args:
        web3 (Web3): Web3 instance connected to the Ethereum network.
        contract_address (str): The Ethereum contract address.
    Returns:
        str: Contract bytecode as a hex string, or None if an error occurs.
    """
    try:
        bytecode = web3.eth.get_code(contract_address).hex()
        return bytecode
    except Exception as e:
        logger.error(f"{Fore.RED}Failed to fetch bytecode: {e}")
        return None


def save_contract_code(contract_data, output_dir):
    """
    Saves the contract source code to the specified directory.
    Supports both single-file and multi-file Solidity contracts.
    Args:
        contract_data (list): Contract source code data fetched from Etherscan.
        output_dir (str): The directory where the contract files will be saved.
    """
    try:
        contract_name = contract_data[0]['ContractName']
        source_code = contract_data[0]['SourceCode']

        # For multi-file contracts (typically Solidity contracts with libraries)
        if source_code.startswith('{{'):
            source_code = source_code[1:-1]  # Clean up string formatting from Etherscan
            source_code_dict = eval(source_code)  # Converts stringified dict to actual dict

            os.makedirs(output_dir, exist_ok=True)

            # Save each file with a progress bar
            with tqdm(total=len(source_code_dict), desc="Saving contract files") as pbar:
                for filename, code in source_code_dict.items():
                    filepath = os.path.join(output_dir, filename)
                    with open(filepath, 'w') as file:
                        file.write(code)
                    logger.info(f"{Fore.GREEN}Saved {filename} to {filepath}")
                    pbar.update(1)

        # For single-file contracts
        else:
            filename = f"{contract_name}.sol"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w') as file:
                file.write(source_code)
            logger.info(f"{Fore.GREEN}Saved {filename} to {filepath}")

    except IOError as e:
        logger.error(f"{Fore.RED}File I/O error: {e}")
    except Exception as e:
        logger.error(f"{Fore.RED}An unexpected error occurred: {e}")


def main():
    """
    Main function that orchestrates the fetching and saving of the contract source code.
    It handles command-line arguments, API calls, bytecode fetching, and saving the files.
    """
    args = setup_argparse()

    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    contract_address = args.contract_address.strip()
    output_dir = args.output_dir

    if not contract_address.startswith("0x") or len(contract_address) != 42:
        logger.error(f"{Fore.RED}Invalid contract address")
        return

    logger.info(f"{Fore.BLUE}Fetching source code for contract at address: {contract_address}")

    web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'))

    if not web3.isConnected():
        logger.error(f"{Fore.RED}Failed to connect to the Ethereum network.")
        return

    # Fetch the contract source code
    contract_data = fetch_contract_source_code(contract_address)

    if contract_data and contract_data[0]['SourceCode']:
        # Save the contract code to files
        save_contract_code(contract_data, output_dir)
    else:
        logger.warning(f"{Fore.YELLOW}Contract source code not verified. Fetching bytecode instead.")
        bytecode = fetch_contract_bytecode(web3, contract_address)
        if bytecode:
            bytecode_filename = os.path.join(output_dir, f"{contract_address}_bytecode.txt")
            with open(bytecode_filename, 'w') as file:
                file.write(bytecode)
            logger.info(f"{Fore.GREEN}Saved contract bytecode to {bytecode_filename}")
        else:
            logger.error(f"{Fore.RED}Failed to retrieve the contract's bytecode.")


if __name__ == "__main__":
    main()
