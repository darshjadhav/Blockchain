#### Module 1 - Create a Blockchain ####

import datetime
import hashlib
import json
from flask import Flask, jsonify

#### Part 1 - Building a Blockchain ####

class Blockchain: # Blockchain object
    def __init__(self): 
        self.chain = [] # Creating a list to store the blocks
        self.create_block(proof = 1, previous_hash = '0') # Creating blocks starting with the genesis block
        
    def create_block(self, proof, previous_hash):  # Creating a dictionary with 4 keys
        block = {'index' : len(self.chain) + 1,  # Creating an index of block
                 'timestamp' : str(datetime.datetime.now()), # Creating a timestamp of when the block was created
                 'proof' : proof,   # Proof of work for the block
                 'previous_hash' : previous_hash}  # Hash that links the blocks in a chain
        
        self.chain.append(block) # Appends the block
        return block
    
    def get_previous_block(self):
        return self.chain[-1] # Last index of the chain returns the last block
    
    def proof_of_work(self, previous_proof):
        new_proof = 1   # Variable which will be incremented until we find the correct proof
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':    # If the string starts with 4 leading zeros then the miner has a valid block
                check_proof = True
            else:
                new_proof += 1  # Increments the proof to go through the while loop again
        return new_proof
            
    def hash(self, block):  # Take input and return a sha256 hash
        encoded_block = json.dumps(block, sort_keys = True).encode() # Formats the block for the sha256 function
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain): # Checks the validity of the previous hash
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain): # Checking if the previous hash is equal to the hash of the previous block
            block = chain[block_index] # Checking current block
            if block['previous_hash'] != self.hash(previous_block): # Checks if previous hash is equal to hash of previous block
                return False # If it isnt equal then return false since it isnt valid
            previous_proof = previous_block['proof'] 
            proof = block['proof']
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000': # Checks to see if the proof starts with 4 leading zeros
                return False
            previous_block = block # Updates the block
            block_index += 1
        return True
    
#### Part 2 - Mining our Blockchain ####

# Creating a Web App #
app = Flask(__name__)
        
# Creating a Blockchain #
blockchain = Blockchain() # Our Blockchain

# Mining a New Block #
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

# Getting the full Blockchain #
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Checking if the Blockchain is valid #
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'The blockchain is valid. :)'}
    else:
        response = {'message': 'Unfortunately, the block chain is NOT valid! :('}
        return jsonify(response), 200
    

# Running the app #
app.run(host = '0.0.0.0', port = 5000)

        