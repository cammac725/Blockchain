import hashlib
import requests

import sys


# TODO: Implement functionality to search for a proof
def proof_of_work(last_proof):
    """
    Simple Proof of Work Algorithm
    Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes
    """
    proof = 0
    
    # TODO: Timer start

    while not valid_proof(last_proof, proof):
        proof += 1

    # TODO: Timer end

    return proof


def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?
    """
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    
    return guess_hash[:6] == "000000"


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one
        r = requests.get(f'{node}/last-proof')
        last_proof = r.response['last_proof']
        new_proof = proof_of_work(last_proof)

        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        
        # When found, POST it to the server {"proof": new_proof}
        if new_proof:
            r.requests.post(f'{node}/mine', json={'proof': new_proof})
            post_response = r.json()
            
            # If the server responds with 'New Block Forged'
        if post_response and post_response['message'] == 'New Block Forged':
            coins_mined += 1
            print(f"{r.status_code} Success! {post_response['message']} /n Coins mined: {coins_mined}")

        else:
            print(f"{r.status_code} Failed to mine coins. /n {post_response['message']}")
       
