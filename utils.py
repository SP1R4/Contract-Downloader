import os
import requests
import logging
import requests_cache
from requests.exceptions import RequestException
from tenacity import retry, stop_after_attempt, wait_fixed
from web3 import Web3

logger = logging.getLogger(__name__)

# Initialize request cache
requests_cache.install_cache('etherscan_cache', expire_after=300)

def validate_contract_address(address):
    if Web3.is_checksum_address(address):
        return address
    return None

@retry(stop=stop_after_attempt(5), wait=wait_fixed(10))
def fetch_contract_source_code(contract_address, retries=5):
    api_key = os.getenv("ETHERSCAN_API_KEY")
    url = f"https://api.etherscan.io/api"
    params = {
        "module": "contract",
        "action": "getsourcecode",
        "address": contract_address,
        "apikey": api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "1":
            return data["result"]
        else:
            logger.warning(f"Error fetching contract source code: {data.get('message')}")
            return None

    except RequestException as e:
        logger.error(f"Network error: {e}")
        return None

def fetch_contract_bytecode(web3, contract_address):
    try:
        bytecode = web3.eth.get_code(contract_address).hex()
        return bytecode
    except Exception as e:
        logger.error(f"Failed to fetch bytecode: {e}")
        return None
