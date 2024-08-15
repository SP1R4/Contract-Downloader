import os
import json
import logging
from tqdm import tqdm

logger = logging.getLogger(__name__)

def save_contract_code(contract_data, output_dir):
    contract_name = contract_data[0]['ContractName']
    source_code = contract_data[0]['SourceCode']
    os.makedirs(output_dir, exist_ok=True)

    if source_code.startswith('{{'):
        source_code_dict = json.loads(source_code[1:-1])
        if 'sources' in source_code_dict:
            sources = source_code_dict['sources']
            for filename, file_data in tqdm(sources.items(), desc="Saving contract files"):
                filepath = os.path.join(output_dir, filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, 'w') as file:
                    file.write(file_data.get('content', ''))
                logger.info(f"Saved {filename} to {filepath}")
    else:
        filepath = os.path.join(output_dir, f"{contract_name}.sol")
        with open(filepath, 'w') as file:
            file.write(source_code)
        logger.info(f"Saved {contract_name}.sol to {filepath}")

def save_contract_bytecode(contract_address, bytecode, output_dir):
    filepath = os.path.join(output_dir, f"{contract_address}_bytecode.txt")
    with open(filepath, 'w') as file:
        file.write(bytecode)
    logger.info(f"Saved contract bytecode to {filepath}")
