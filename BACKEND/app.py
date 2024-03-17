# Run dev with `python app.py` (on this code) and `http-server` (for the frontend)

from flask import Flask, jsonify, request, render_template, send_file, send_from_directory
import json
import flask
from btcvalidator import isValidBTCAddress #Won't work on signet, so comment out testing
import threading
import logging
import subprocess
import signal
import os
import sys

#app = Flask(__name__,static_folder='../frontend')
app = Flask(__name__,
    static_url_path='',
    static_folder='../FRONTEND/'
)
from flask_cors import CORS,cross_origin  # comment this on deployment
CORS(app)  # comment this on deployment

# Create the locks for concurrent requests
lock = threading.Lock()

# Create the database logger for addresses
logger = logging.getLogger('addies')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('../data/pending_buys.txt')
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

loginscribes = logging.getLogger('inscribing')
loginscribes.setLevel(logging.DEBUG)
handler_loginscribes = logging.FileHandler('../data/pending_inscribes.txt')
handler_loginscribes.setLevel(logging.DEBUG)
loginscribes.addHandler(handler_loginscribes)

# Create the general logger
printer = logging.getLogger(__name__)
printer.setLevel(logging.DEBUG)
printerhandler = logging.FileHandler('../data/log.log')
printerhandler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
printerhandler.setFormatter(formatter)
printer.addHandler(printerhandler)
printer.debug("Success!")

pids = []
    
print("Flask app running, awaiting requests...")

'''
a signal handler function that will be called when the SIGTERM signal is received. This 
function sends a SIGTERM signal to the subprocess using os.kill and then exits the 
Python script using sys.exit(0).
'''
def signal_handler(sig, frame):
    # Print a message indicating that the script has received a SIGTERM signal
    printer.debug('Received SIGTERM, killing subprocess...')
    # Iterate over each process ID in the list of pids
    for pid in pids:
        # Send a SIGTERM signal to the process with the given pid
        os.kill(pid, signal.SIGTERM)
    # Exit the script with a status code of 0
    sys.exit(0)

'''
Helper function to open a file a convert to a python dictionary
'''
def create_dict_from_file(filename):
    # Check if the file is empty
    if os.stat(filename).st_size == 0:
        return {}

    # Initialize an empty dictionary to store the key-value pairs
    result = {}

    # Open the file for reading using a context manager
    with open(filename, 'r') as f:
        # Iterate over each line in the file
        for line in f:
            # Split the line into two strings using whitespace as the separator
            # and assign them to the variables key and value
            # value, key = line.strip().split()
            splitline = line.strip().split() #depoist, receive, inscrip
            value = [splitline[0], splitline[2]] 
            key = splitline[1]
            # Add the key-value pair to the dictionary
            result[key] = value

    # Return the resulting dictionary
    return result

    
'''
Method to handle buying/inscribing/sending inscriptions in a "lazy" way.
No inscription number (i.e sequential file names in a collection) is specified.
'''
@app.route('/post_inscribe', methods=['POST'])
def post_inscribe():
   
    with lock:
        # Get the data sent from the server
        btcreceive = request.get_json()
        receive_address = btcreceive["data"]
        # inscription_id = str(btcreceive["id"])
        printer.debug(f"post_inscribe: Received receiver-address: {receive_address}, for new inscription.")

        # Get the current dict of addresses
        assigned_addresses = create_dict_from_file('../data/pending_inscribes.txt')

         # If we have seen this receiver-address before then....
        if receive_address in assigned_addresses:
            printer.debug("post_inscribe: Found exisiting receiver-address!")
            # Give them back the deposit-address they had before
            deposit_address = assigned_addresses[receive_address]

            # TODO: Go see if they have transactions pending, etc...
            # Print return them to the display etc .
            return_data = {
                "status": "success",
                "message": f"Found exisiting receiver-address!",
                "address": deposit_address
            }

            return flask.Response(response=json.dumps(return_data), status=201)
    
        #Otherwise, assume it is and continue
        # if isValidBTCAddress(receive_address):
        #     pass
        # else:
        #     return_data = {
        #             "status": "FAIL",
        #             "message": f"Not a valid BTC address to send your Ordinal Inscription to.",
        #             "address": None
        #         }

        #     return flask.Response(response=json.dumps(return_data), status=201)

        printer.debug("post_inscribe: Writing dep-rec addresses to log and launching ord!")
        # Then run the wallet watcher which will handle the payment and inscribing.
        # Open output file, named approriately
        with open("../data/watching_inscribes/receive-watch_"+deposit_address+"_"+receive_address+".txt", 'w+') as output_file:
            # Run a bash script with the addresses as argument
            process  = subprocess.Popen(['/bin/bash','./wallet_watcher_inscribe.sh',deposit_address,receive_address], stdout=output_file, stderr=subprocess.STDOUT)
            pid = process.pid
            pids.append(pid)
            printer.debug(f"post_inscribe: Running! Depoits-address: {deposit_address} Receive-address: {receive_address} Process: {pid}")

            # Register the signal handler for SIGTERM
            signal.signal(signal.SIGTERM, signal_handler)

            # Write the deposit_address and receive_address to a file
            loginscribes.debug(deposit_address + ' ' + receive_address + ' ' + str(pid))

        # Return the deposit-address to the client as a JSON object.
        return_data = {
            "status": "success",
            "message": f"Receiver-address pending, returning a deposit-address.",
            "transactionNumber": deposit_address
        }

        return flask.Response(response=json.dumps(return_data), status=201)


@app.route('/hello')
def hello():
    print("hello")
    return jsonify({'message': 'Hello from Flask!'})


# @app.route("/get_update", methods=["GET"])
# def getUpdate():
#     return flask.Response(response=json.dumps({"message":"get got"}), status=201)

# '''
# Returns a deposit-address to the pool of available deposit addresses.
# This may be because a user has timed-out (not deposited funds in time)
# or something else. We must be careful about this and give enough time for
# a confirmation. Perhaps some imposed transaction verification to assume no silly buggers.
# '''
# @app.route("/release_deposit_address", methods=["POST"])
# def release_address():
#     global available_addresses, reserved_addresses, assigned_addresses

#     # Get the address to release from the JSON payload of the POST request
#     deposit_address = request.json["address"]

#     # Check if the address is currently reserved (i.e. in use by a client)
#     if deposit_address in reserved_addresses:
#         # Remove the deposit-address from the reserved list and add it back to the available list
#         reserved_addresses.remove(deposit_address)
#         available_addresses.append(deposit_address)
#         assigned_addresses.pop(deposit_address)

#     # Return a JSON object with a single "success" property to indicate that the release was successful
#     return jsonify({"success": True})


'''
Method to provide list of images in collection
'''
IMAGES_DIR = 'images/'

@app.route('/images',methods=["GET"])
def get_images():
    # Get a list of all image files in the directory
    image_files = [f for f in os.listdir(IMAGES_DIR) if f.endswith('.png')]

    # Generate a list of image objects with ids and availability status
    images = [{'id': i+1, 'available': True} for i in range(len(image_files))]

    with open('../data/pending_buys.txt', 'r') as f:
        unavailable = [line.split()[2] for line in f]   

    # Check if each image file exists and set the availability status accordingly
    for image in images:
        if str(image['id']) in unavailable:
            image['available'] = False

    # Return the list of image objects as a JSON response
    return jsonify(images)

@app.route('/images/<int:image_id>.png',methods=["GET"])
def get_image(image_id):
    # Generate the path to the image file
    image_path = os.path.join(IMAGES_DIR, f'{image_id}.png')

    # If the image file exists, send it as a response with the correct MIME type
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/png')

    # Otherwise, return a 404 error response
    return jsonify({'error': 'Image not found'}), 404


'''
Method to handle sending inscriptions (could be as an escrow service).
Pulls a deposit-address from the premade list of addresses.
Gives a user one of these addresses semi-permently attached to their 
provided receiver-address.
When a new receiver-address is obtained, it is written to a file which
initiates the inscription and sending functions.
'''
@app.route('/post_send', methods=['POST'])
def post_send():
   
    with lock:
        # Get the data sent from the server
        btcreceive = request.get_json()
        receive_address = btcreceive["data"]
        inscription_id = str(btcreceive["id"])
        printer.debug(f"Received receiver-address: {receive_address}, for inscription id: {inscription_id}")

        # Check if the inscription is available.
        with open('../data/pending_buys.txt', 'r') as f:
            pending_buys = [line.split()[2].strip() for line in f.readlines()]

        if inscription_id in pending_buys:
            return_data = {
                "status": "Fail",
                "message": f"Inscription is in escrow!",
                "address": None
            }

            return flask.Response(response=json.dumps(return_data), status=201)
        
        #Otherwise, assume it is and continue
        # if isValidBTCAddress(receive_address):
        #     pass
        # else:
        #     return_data = {
        #             "status": "FAIL",
        #             "message": f"Not a valid BTC address to send your Ordinal Inscription to.",
        #             "address": None
        #         }

        #     return flask.Response(response=json.dumps(return_data), status=201)

        #Generate a depoist address, use ord or bitcoin cli?
        # deposit_address = "5"
        deposit_address = subprocess.getoutput("ord --signet --cookie-file /home/ubuntu/signet/signet/.cookie wallet receive | jq -r '.address'")
        # deposit_address = subprocess.getoutput('bitcoin-cli -signet -rpccookiefile=/home/ubuntu/signet/signet/.cookie getnewaddress "" "bech32m"')

        printer.debug("Writing dep-rec addresses to log and launching ord!")

        # Then run ord send!
        # Open output file, named approriately
        with open("../data/watching_send/receive-watch_"+deposit_address+"_"+receive_address+".txt", 'w+') as output_file:
            # Run a bash script with the addresses as argument
            process  = subprocess.Popen(['/bin/bash','./wallet_watcher_send.sh',deposit_address,receive_address,inscription_id], stdout=output_file, stderr=subprocess.STDOUT)
            pid = process.pid
            pids.append(pid)
            printer.debug(f"Running! Depoits-address: {deposit_address} Receive-address: {receive_address} Process: {pid}")

            # Register the signal handler for SIGTERM
            signal.signal(signal.SIGTERM, signal_handler)

            # Write the deposit_address and receive_address to a file
            logger.debug(deposit_address + ' ' + receive_address + ' ' + inscription_id + ' ' + str(pid))

        # Return the deposit-address to the client as a JSON object.
        return_data = {
            "status": "success",
            "message": f"Receiver-address pending, returning a deposit-address.",
            "transactionNumber": deposit_address
        }

        return flask.Response(response=json.dumps(return_data), status=201)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
