import socket
from typing_extensions import dataclass_transform                                         
from cryptography.fernet import Fernet
import os
import json
import pickle as pk

def json_format(data): #function for json
    data = json.loads()

def binary_format(data): #function for binary
    data = pk.loads()

def xml_format(data): # function for XML(temporary)
    data = 1

def decrypt_file(filename):
    key = open("key.key", "rb").read()
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(filename, "wb") as file:
        file.write(decrypted_data)

def output_console(file_name):
    with open(file_name,'r') as viewFileOpen:
        data = viewFileOpen.read()
    print(data)

def main():
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

    # create a socket object
    serversocket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = socket.gethostname()                           
    port = 29999                                           

    # bind to the port
    try:
        serversocket.bind((host, port))
        print("Socket bind successful")
    except:
        print("Unable to bind socket")
        exit(0)

    # queue up to 5 requests
    serversocket.listen(5)

    while True:
        # establish a connection
        clientsocket,addr = serversocket.accept()      
        print("Connection received from %s" % str(addr))

        # Receive parameters from client
        file_type = clientsocket.recv(1).decode('utf-8')
        file_encrypted = clientsocket.recv(1).decode('utf-8')
        file_name = clientsocket.recv(100).decode('utf-8')
        file_pickling = clientsocket.recv(1).decode('utf-8')

        print("\nFile type: " + file_type)
        print("Pickling: " + file_pickling)
        print("File encrypted: " + file_encrypted)
        print("Filename: " + file_name)
        
        #Delete previous file
        if os.path.exists(file_name):
            os.remove(file_name)

        with open(file_name, 'wb') as f:
            while True:
                data = clientsocket.recv(1024)
                if not data:
                    break
                # write data to a file
                f.write(data)
        f.close()
        print("\nReceived data\n")

        if output_type.lower() == "f":
            print("File written to server")

        if clientsocket.recv(1).decode('utf-8') == "1": # for JSON format pick
            json_format(data)
        
        if clientsocket.recv(1).decode('utf-8') == "2": # for binary format pick
            binary_format(data)
        
        if clientsocket.recv(1).decode('utf-8') == "3": # for XML format pick
            xml_format(data)

        #Decrypt file if required
        if file_encrypted == "y":
            decrypt_file(file_name)

        #Output to console
        if output_type.lower() == "c":
            print("Contents of file:")
            output_console(file_name)
            #Remove file - only want it in console
            if os.path.exists(file_name):
                os.remove(file_name)

        clientsocket.close()
        print("\nClosing server")
        break

if __name__ == "__main__":
    main()