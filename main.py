import os
import logging
import argparse
from logger import setup_logging
from utils import fetch_contract_source_code, fetch_contract_bytecode, validate_contract_address
from handlers import save_contract_code, save_contract_bytecode
from dotenv import load_dotenv
from web3 import Web3

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logging()

def setup_argparse():
    parser = argparse.ArgumentParser(description="Fetch and save verified contract source code from Etherscan.")
    parser.add_argument("contract_address", type=str, help="The Ethereum address of the contract.")
    parser.add_argument("-o", "--output-dir", default="contracts", type=str, help="Directory to save the contract files.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity.")
    parser.add_argument("--retry", type=int, default=5, help="Number of retries for fetching source code (default: 5).")
    parser.add_argument("--no-cache", action="store_true", help="Disable caching of API responses.")
    return parser.parse_args()

def main():
    args = setup_argparse()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    contract_address = validate_contract_address(args.contract_address)
    if not contract_address:
        logger.error("Invalid contract address.")
        return

    output_dir = args.output_dir
    retry_attempts = args.retry

    web3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{os.getenv("INFURA_API_KEY")}'))

    if not web3.is_connected():
        logger.error("Failed to connect to Ethereum network.")
        return

    # Fetch contract source code
    contract_data = fetch_contract_source_code(contract_address, retry_attempts)

    if contract_data and contract_data[0].get('SourceCode'):
        save_contract_code(contract_data, output_dir)
    else:
        logger.warning("Contract source code not verified. Fetching bytecode instead.")
        bytecode = fetch_contract_bytecode(web3, contract_address)
        if bytecode:
            save_contract_bytecode(contract_address, bytecode, output_dir)
        else:
            logger.error("Failed to retrieve the contract's bytecode.")

if __name__ == "__main__":
    main()
