"""This module runs a client program for sending data to a
server program.
The client can send a text file or dictionary.
The text file can be sent encrypted and the dictionary can be
pickled as JSON, binary or XML format.
"""

import socket
import json
import pickle as pk
import time
import shutil
import os
import sys
from xml.etree.ElementTree import Element, tostring
from cryptography.fernet import Fernet

# Definition of dictionary to be sent to server
data = {
    'Group': 'B',
    'Program':'Client Server',
    'Task':'Send dictionary'
}

json_pick = json.dumps(data) # pickle JSON format
binary_pick = pk.dumps(data) # pickle binary format
xml_pick = Element('data') # pickle XML format
for key, value in data.items(): # convert key and value to XML format
    child_node = Element(key)
    child_node.text = value
    xml_pick.append(child_node)

def generate_key():
    """Generate fernet key for encryption and decryption."""
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def encrypt_file(filename):
    """Encrypt text file and create backup file.
    Argument:
        filename: file to be encrypted.
    """
    key = open("key.key", "rb").read()
    fkey = Fernet(key)
    dest = filename + "backup"
    shutil.copy(filename, dest)
    with open(filename, "rb") as file:
        file_data = file.read()
    encrypted_data = fkey.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)

def main():
    """This main client function sends the selected data to the server.
    There are no arguments to run the function and all parameters are
    set at runtime by the user.
    """
    # User input to select text file or dictionary
    while True:
        file_type = input("File type: Text file(t) or Dictionary(d)? ")
        if file_type.lower() == "t":
            print("Input is text file")
            break
        elif file_type.lower() == "d":
            print("Input is dictionary")
            break
        else:
            print("invalid selection")

    # User input to select dictionary pickling format
    if file_type == "d":
        while True:
            msg_pickling = print("Choose pickling format")
            msg_pickling = input("1, JSON\n"
                    "2, Binary\n"
                    "3, XML\n"
                    "Choose 1 for JSON, 2 for Binary format, 3 for XML : ")
            # JSON pickling format
            if str(msg_pickling) == "1":
                file_name = "jsonfile.txt"
                sendmesg = str.encode(json_pick)
                break
            # Binary pickling format
            elif str(msg_pickling) == "2":
                file_name = "binaryfile.txt"
                sendmesg = binary_pick
                break
            # XML pickling format
            elif str(msg_pickling) == "3":
                file_name = "xmlfile.txt"
                sendmesg = tostring(xml_pick)
                break
            else:
                print("invalid selection")
    else:
        msg_pickling = "0" # Default to unused value if text file

    # User input select encryption on text file
    if file_type == "t":
        file_name = "textfile.txt"
        if os.path.exists(file_name):
            while True:
                file_encrypted = input("Encrypt file (y/n)? ")
                if file_encrypted.lower() == "y":
                    print("File will be encrypted")
                    break
                elif file_encrypted.lower() == "n":
                    print("File will not be encrypted")
                    break
                else:
                    print("invalid selection")
        else:
            sys.exit(file_name + " does not exist.")
    else:
        file_encrypted = "n" # Default to no encryption if dictionary

    # Run file encryption
    if file_encrypted == "y":
        encrypt_file(file_name)

    # Create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host = socket.gethostname()
    port = 29999

    # Connect to hostname on the port.
    client.connect((host, port))
    print("Connected to server")

    # Send user inputs to server
    client.send(file_type.encode('utf-8'))
    client.send(msg_pickling.encode('utf-8'))
    client.send(file_encrypted.encode('utf-8'))
    client.send(file_name.encode('utf-8'))

    # Wait for previous data to be sent to server
    time.sleep(2)

    # Send text file to server
    if file_type == "t":
        file = open(file_name,'rb')
        data = file.read(1024)
        while data:
            client.send(data)
            data = file.read(1024)
        file.close()
    # Send dictionary data to server
    elif file_type == "d":
        print("Pickled data: " + str(sendmesg))
        client.send(sendmesg)

    # Copy original text file over encrypted text file
    if file_encrypted == "y":
        backup = file_name + "backup"
        shutil.copy(backup, file_name)
        os.remove(backup)

    # Close client connection
    client.close()

    print("Completed sending data to server")

if __name__ == "__main__":
    main()
