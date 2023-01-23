from flask import jsonify
from chain import Blockchain

def mine_block(blockchain: Blockchain, node_address, receiver):
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash_function(previous_block)
    blockchain.add_transaction(node_address, receiver, 1)      # mining reward
    new_block = blockchain.create_block(proof, previous_hash)

    response = {
        'message': 'New block mined and added!',
        'index': new_block['index'],
        'timestamp': new_block['timestamp'],
        'proof': new_block['proof'],
        'previous_hash': new_block['previous_hash'],
        'transactions': new_block['transactions']
    }

    return jsonify(response), 200