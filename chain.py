import datetime
import hashlib
import json
import requests
from urllib.parse import urlparse

# Class for the blockchain
class Blockchain:

    # Constructor, to be used while creating an entirely new blockchain
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes = set()

    # Create a new block
    def create_block(self, proof: int, previous_hash):
        block = {
            'index': len(self.chain),
            'timestamp': datetime.datetime.now(datetime.timezone.utc).strftime("%d-%m-%Y %H:%M:%S:%f"),
            'proof': proof,
            'previous_hash': previous_hash,
            'transactions': self.transactions
        }
        self.transactions = []
        self.chain.append(block)
        return block

    # Get the last block
    def get_previous_block(self):
        return self.chain[-1]

    # Checking if proof (nonce) is valid, and mining was successful
    def proof_of_work(self, previous_proof):
        new_proof = 1           # nonce
        check_proof = False

        while check_proof is False:
            hash_result = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest() # Hash function of PoW
            if hash_result[:4] == '0000':
                check_proof = True
            else:
                new_proof +=1

        return new_proof

    # Hash function of the chain
    def hash_function(self, block):
        encoded_block = json.dumps(block, sort_keys=True, default = str).encode()
        hash_result = hashlib.sha256(encoded_block).hexdigest()

        return hash_result

    # Function to check if the chain is valid
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index<len(chain):
            current_block = chain[block_index]

            # Check 1 - Checking if previous hash stored in current block is equal to the hash result on inputting the previous block
            stored_previous_hash = current_block['previous_hash']
            actual_previous_hash = self.hash_function(previous_block)
            if actual_previous_hash != stored_previous_hash:
                return False
            
            previous_proof = previous_block['proof']
            current_proof = current_block['proof']

            # Check 2 - Checking if the PoW hash operation yielded a larger number than '0000...' at any point
            if hashlib.sha256(str(current_proof**2 - previous_proof**2).encode()).hexdigest()[:4] != '0000':
                return False

            previous_block = current_block
            block_index += 1

        return True
    
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })

        previous_block = self.get_previous_block()
        return previous_block['index']+1

    def add_node(self, address):
        parsed_address = urlparse(address)
        self.nodes.add(parsed_address.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                response_json = response.json()
                length = response_json['length']
                chain = response_json['chain']
                if length>max_length and self.is_chain_valid(chain):
                    longest_chain = chain
                    max_length = length
        if longest_chain:
            self.chain = longest_chain
            return True
        return False