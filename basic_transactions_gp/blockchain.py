import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # self.used_proofs = {}
        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            # TODO
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.last_block)
        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the chain to the block
        self.chain.append(block)
        # Return the new block
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })

        return self.last_block["index"]

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It converts the Python string into a byte string.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        # TODO: Create the block_string
        block_string = json.dumps(block, sort_keys=True) # <- making sure it's always sorted and order doesn't change

        # TODO: Hash this string using sha256
        raw_hash = hashlib.sha256(block_string.encode())
        hex_hash = raw_hash.hexdigest()

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # TODO: Return the hashed block string in hexadecimal format
        return hex_hash

    @property
    def last_block(self):
        return self.chain[-1]

    # def proof_of_work(self, block):
    #     """
    #     Simple Proof of Work Algorithm
    #     Stringify the block and look for a proof.
    #     Loop through possibilities, checking each one against `valid_proof`
    #     in an effort to find a number that is a valid proof
    #     :return: A valid proof for the provided block
    #     """
    #     # TODO
    #     proof = 0

    #     block_string = json.dumps(block, sort_keys=True)

    #     while self.valid_proof(block_string, proof) is False:
    #         proof +=1
    #     # return True or False

    #     return proof

    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the 
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        # TODO
        guess = f"{block_string}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:6] == "000000"


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

# old mine function
# @app.route('/mine', methods=['GET'])
# def mine():
#     # Run the proof of work algorithm to get the next proof
#     proof = blockchain.proof_of_work(blockchain.last_block)

#     # Forge the new Block by adding it to the chain with the proof
#     previous_hash = blockchain.hash(blockchain.last_block)
#     block = blockchain.new_block(proof, previous_hash)


#     response = {
#         "new_block": block
#     }

#     return jsonify(response), 200


@app.route('/mine', methods=['POST'])
def mine():
    # get data from request
    data = request.get_json()

    # check if required fields are included
    if data and "id" not in data or "proof" not in data:
        print('test')   
        error = {
            "err": "You are missing required fields"
        }

        return jsonify(error), 400
    
    else:
        # define block string
        block_string = json.dumps(blockchain.last_block, sort_keys=True)
        
        #if provided proof is valid
        if blockchain.valid_proof(block_string, data["proof"]):
            # Forge the new Block by adding it to the chain with the proof
            previous_hash = blockchain.hash(blockchain.last_block)
            block = blockchain.new_block(data["proof"], previous_hash)

            response = {
                "message": "New Block Forged",
                "new_block": block
            }

            blockchain.new_transaction('0', data["id"], '1')

            return jsonify(response), 200
        else:
            error = {
                "err": "The proof is invalid or has previously been used"
            }

            return jsonify(error), 400


@app.route('/chain', methods=['GET'])
def full_chain():
    print('check')
    response = {
        # TODO: Return the chain and its current length
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

# returning last block in chain
@app.route('/last-block', methods=['GET'])
def last_block():
    response = {
        # TODO: Return the chain and its current length
        'last_block': blockchain.last_block,
    }
    return jsonify(response), 200



@app.route('/transactions/new', methods=['POST'])
def transaction():
     # get data from request
    data = request.get_json()

    if data and "sender" not in data or "recipient" not in data or "amount" not in data:
        error = {
            "err": "You are missing required fields"
        }

        return jsonify(error), 400
    
    else:
        blockchain.new_transaction(data["sender"], data["recipient"], data["amount"])
        response = {
            # TODO: Return the chain and its current length
            'message': f"Success. Transaction located in block {blockchain.last_block}",
        }

        return jsonify(response), 200

# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
