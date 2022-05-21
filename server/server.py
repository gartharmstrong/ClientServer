"""This module runs a server program for receivnig data from a
client program.
The server can output the received data to the console or to a file.
The server will handle the received data according to parameters
received from the client. These include encryption and pickling.
"""

import socket
import os
import json
import pickle as pk
import xml.etree.ElementTree as et
import xmltodict
from cryptography.fernet import Fernet

def json_format(file_name):
    """Writes unpickled JSON data to file.
    Argument:
        file_name: file containing pickled JSON data.
    """
    with open(file_name, 'r') as pkfile:
        unpickled = json.loads(pkfile.read())
    with open(file_name, 'w') as unpkfile:
        unpkfile.write(str(unpickled))

def json_dict(file_name):
    """Returns unpickled JSON data.
    Argument:
        file_name: file containing pickled JSON data.
    """
    with open(file_name, 'r') as dictfile:
        unpickled = json.loads(dictfile.read())
    return unpickled

def binary_format(file_name):
    """Writes unpickled binary data to file
    Argument:
        file_name: file containing pickled binary data.
    """
    with open(file_name,'rb') as pkfile:
        unpickled = pk.load(pkfile)
    with open(file_name, 'w') as unpkfile:
        unpkfile.write(str(unpickled))

def binary_dict(file_name):
    """Returns unpickled binary data.
    Argument:
        file_name: file containing pickled binary data.
    """
    with open(file_name, 'rb') as pkfile:
        unpickled = pk.load(pkfile, encoding='utf-8')
        return unpickled

def xml_format(file_name): # function for XML
    """Writes unpickled XML data to file
    Argument:
        file_name: file containing pickled XML data.
    """
    with open(file_name,'r') as pkfile:
        unpickled = et.parse(pkfile)
        root = unpickled.getroot()
        write_file = et.tostring(root)
        xml_decode = write_file.decode()
        xml_datadict = xmltodict.parse(xml_decode) # Convert XML to dict
        xml_dict = dict(xml_datadict.pop('data')) # Retrieves 'data' values
    with open(file_name, 'w',) as unpkfile:
        unpkfile.write(str(xml_dict))

def xml_format_dict(file_name):
    """Returns unpickled XML data.
    Argument:
        file_name: file containing pickled XML data.
    """
    with open(file_name,'r') as pkfile:
        unpickled = et.parse(pkfile)
        root = unpickled.getroot()
        write_file = et.tostring(root)
        xml_decode = write_file.decode()
        xml_datadict = xmltodict.parse(xml_decode) # Convert XML to dict
        xml_dict = dict(xml_datadict.pop('data')) # Retrieves 'data' values
        return xml_dict

def decrypt_file(filename, output_type):
    """Receives encrypted text file and overwrites with decrypted data.
    Arguments:
        filename: file to be encrypted.
        output_type: output data to console or file.
    """
    key = open("key.key", "rb").read()
    fkey = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fkey.decrypt(encrypted_data)
    if output_type == "c":
        print("\nDecrypted data: \n" + decrypted_data.decode("utf-8"))
    with open(filename, "wb") as file:
        file.write(decrypted_data)

def output_console(file_name):
    """Output file contents to console
    Argument:
        file_name: file to be output to console.
    """
    with open(file_name,'r') as file_open:
        data = file_open.read()
    print(data)

def main():
    """This main server function receives data from the client program.
    There are no arguments to run the function and all parameters are
    set at runtime by the user.
    """
    # Create a socket object
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host = socket.gethostname()
    port = 29999

    # Bind to the port
    try:
        serversocket.bind((host, port))
        print("Socket bind successful")
    except:
        print("Unable to bind socket")
        exit(0)

    # User input to output received data to console or file
    while True:
        output_type = input("Output to File(f) or Console(c)? ")
        if output_type.lower() == "f":
            print("Output to file\n")
            break
        elif output_type.lower() == "c":
            print("Output to console\n")
            break
        else:
            print("invalid selection\n")


    # Queue up to 5 requests
    serversocket.listen(5)
    print("Waiting for client to receive data ..")

    while True:
        # Establish connection with client
        clientsocket,addr = serversocket.accept()
        print("Connection received from %s" % str(addr))

        # Receive data parameters from client
        file_type = clientsocket.recv(1).decode('utf-8')
        file_pickling = clientsocket.recv(1).decode('utf-8')
        file_encrypted = clientsocket.recv(1).decode('utf-8')
        file_name = clientsocket.recv(100).decode('utf-8')

        print("\nFile type: " + file_type)
        print("Pickling: " + file_pickling)
        print("File encrypted: " + file_encrypted)
        print("Filename: " + file_name)

        # Delete old data file if it exists
        if os.path.exists(file_name):
            os.remove(file_name)

        # Receive text file or dictionary data from client
        with open(file_name, 'wb') as rec_file:
            while True:
                data = clientsocket.recv(1024)
                if not data:
                    break
                # Write data to a file
                rec_file.write(data)
        rec_file.close()
        print("\nReceived data\n")

        # Unpickle dictionary data to file
        if output_type.lower() == "f":
            if file_pickling == "1": # JSON data
                json_format(file_name)
            elif file_pickling == "2":  # Binary data
                binary_format(file_name)
            elif file_pickling == "3":  # XML data
                xml_format(file_name)
            print("File written to server")

        # Output data to console
        elif output_type.lower() == 'c':
            # Unpickle JSON data and output to console
            if file_pickling == "1":
                data_json = json_dict(file_name)
                with open(file_name, 'r') as file_json:
                    contents = file_json.read()
                print(type(data_json))
                print("Contents of data: \n{}".format(contents))
                if os.path.exists(file_name):
                    os.remove(file_name)

            # Unpickle binary data and output to console
            elif file_pickling == "2":
                data_binary = binary_dict(file_name)
                print(type(data_binary))
                print("Contents of data:  \n ",data_binary)
                if os.path.exists(file_name):
                    os.remove(file_name)

            # Unpickle XML data and output to console
            elif file_pickling == "3":
                xml_file = xml_format_dict(file_name)
                print(type(xml_file))
                print("Contents of data:  \n ",xml_file)
                if os.path.exists(file_name):
                    os.remove(file_name)

            # Output text file to console
            elif file_type == "t":
                print("Contents of text file:")
                output_console(file_name)

        # Decrypt text file if required
        if file_encrypted == "y":
            decrypt_file(file_name, output_type)
        # Delete text file if output to console
        if file_type == "t" and output_type == "c":
            os.remove(file_name)

        # Close connection from client
        clientsocket.close()
        print("\nClosing server")
        break

if __name__ == "__main__":
    main()
