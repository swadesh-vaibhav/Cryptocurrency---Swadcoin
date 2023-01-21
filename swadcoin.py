# Creating a cryptocurrency swadcoin

from flask import Flask, jsonify, request
from uuid import uuid4
from chain import Blockchain
from mining import mine_block

# Creating Web App for APIs
app = Flask(__name__)

# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace('-', '')

# Create the blockchain
blockchain = Blockchain()

# Route to mine a new block
@app.route('/mine_block', methods = {'GET'})
def mine_block_endpoint():
    response = mine_block(blockchain, node_address)
    return response

# Route to add a new transaction to the chain
@app.route('/add_transaction', methods = {'POST'})
def add_transaction_endpoint():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    for key in transaction_keys:
        if key not in json:
            response = {'message': f"'{key}' information missing in POST request json"}
            http_code = 400
            return jsonify(response), http_code
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
    response = {'message':f"Transaction will be added into block at index {index}"}
    return jsonify(response), 200
    
# Route to connect a new node
@app.route('/connect_nodes', methods = {'POST'})
def connect_nodes():
    json = request.get_json
    nodes = json['nodes']
    if nodes is None:
        response = {
            'message':'No node in input'
        }
        response_code = 400
    else:
        for node in nodes:
            blockchain.add_node(node)
        response = {
            'messsage':'All the nodes are now connected',
            'nodes':list(blockchain.nodes)
            }
        response_code = 200
    return jsonify(response), response_code

# Route to get the entire chain
@app.route('/get_chain', methods = {'GET'})
def get_chain():
    response = {
        'length': len(blockchain.chain),
        'chain': blockchain.chain
    }
    
    return jsonify(response, 200)

# Route to replace the chain by the longest chain
@app.route('/replace_chain', methods = {'GET'})
def replace_chain():
    old_chain = blockchain.chain
    is_chain_replaced = blockchain.replace_chain()
    if(is_chain_replaced):
        response = {
            "message":"The node has been updated with the longest chain",
            "old_chain":old_chain,
            "new_chain":blockchain.chain,
            }
    else:
        response = {
            "message":"Already the longest chain",
            "old_chain":old_chain,
            "new_chain":blockchain.chain,
            }

    return jsonify(response, 200)

# Route to check if the chain is valid
@app.route('/check_valid', methods = {'GET'})
def check_valid():
    validity = blockchain.is_chain_valid()
    response = {
        'validity' : validity
    }

    return jsonify(response, 200)

app.run(host = '0.0.0.0', port = 5000, debug = True)