import os
from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_typed_data
from dotenv import load_dotenv
from .chain_utils import get_rpc_url, get_chain_name


class Wallet(object):
    def __init__(self, chainId):
        self.chainId = chainId
        chain_name = get_chain_name(chainId)
        chain_rpc = get_rpc_url(chainId)
        if chain_name and chain_rpc:
            self.w3 = Web3(Web3.HTTPProvider(chain_rpc))
            if not self.w3.is_connected():
                raise Exception(f"Failed to connect to {chain_name} network")
        else:
            raise Exception(f"No information found for {chain_name}. Please check chain configs.")
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        dotenv_path = os.path.join(os.path.dirname(cur_dir), '.env')
        load_dotenv(dotenv_path)

    def call_contract(self, contractAddress, inputData, value):
        private_key = os.getenv('PRIVATE_KEY')
        account = Account.from_key(private_key)
        contract_address = self.w3.to_checksum_address(contractAddress)

        transaction = {
            'to': contract_address,
            'value': int(value),
            'gas': 200000,
            'gasPrice': 2*self.w3.eth.gas_price,
            'nonce': self.w3.eth.get_transaction_count(account.address),
            'data': inputData,
            'chainId': int(self.chainId)
        }

        signed_txn = account.sign_transaction(transaction)

        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"Transaction sent: {tx_hash.hex()}")

        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        # print(f"Transaction confirmed in block {tx_receipt.blockNumber}")

        if tx_receipt.status == 1:
            message = f"Transaction was successful: {tx_hash.hex()}"
        else:
            message = f"Transaction failed: {tx_hash.hex()}"
        return message

    def get_signed_sign(self, full_message):
        private_key = os.getenv('PRIVATE_KEY')
        account = Account.from_key(private_key)
        signable_message = encode_typed_data(full_message=full_message)
        signed_message = account.sign_message(signable_message)
        return signed_message.signature.hex()