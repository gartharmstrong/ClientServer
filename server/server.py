import socket                                       
from cryptography.fernet import Fernet
import os
import json
import pickle as pk

def json_format(file_name): #function for json
    with open(file_name, 'r') as pkfile:
        unpickled = json.loads(pkfile.read())
    with open(file_name, 'w') as unpkfile:
        unpkfile.write(str(unpickled))

def json_dict(file_name): #function for json <class 'dict'>
    with open(file_name, 'r') as dictfile:
        unpickled = json.loads(dictfile.read())
    return unpickled

def binary_format(file_name): #function for binary
    with open(file_name,'rb') as pkfile:
        unpickled = pk.load(pkfile)
    with open(file_name, 'w') as unpkfile:
        unpkfile.write(str(unpickled))
        
def binary_dict(file_name): #function for binary
    with open(file_name, 'rb') as pkfile:
        unpickled = pk.load(pkfile, encoding='utf-8')
        return unpickled


def xml_format(data): # function for XML(temporary)
    data = 1

def decrypt_file(filename, output_type):
    key = open("key.key", "rb").read()
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    if output_type == "c":
        print("\nDecrypted data: \n" + decrypted_data.decode("utf-8"))
    with open(filename, "wb") as file:
        file.write(decrypted_data)

def output_console(file_name):
    with open(file_name,'r') as viewFileOpen:
        data = viewFileOpen.read()
    print(data)

def main():
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


    # queue up to 5 requests
    serversocket.listen(5)
    print(f"Waiting for client to receive data ..")

    while True:
        # establish a connection
        clientsocket,addr = serversocket.accept()      
        print("Connection received from %s" % str(addr))

        # Receive parameters from client
        file_type = clientsocket.recv(1).decode('utf-8')
        file_pickling = clientsocket.recv(1).decode('utf-8')
        file_encrypted = clientsocket.recv(1).decode('utf-8')
        file_name = clientsocket.recv(100).decode('utf-8')

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
            # User choose to print in file
            if file_pickling == "1": # for json format pick to file
                json_format(file_name)
            elif file_pickling == "2":  # for binary format pick to file
                binary_format(file_name)
            elif file_pickling == "3":  # for XML format pick to file
                xml_format(data)
            print("File written to server")
        
        elif output_type.lower() == 'c':
            # User choose to print on console
            if file_pickling == "1": # for json format pick class dictionary
                data_json = json_dict(file_name)
                with open(file_name, 'r') as f:
                    c = f.read()
                print(type(data_json))
                print("Contents of data: \n{}".format(c))
                if os.path.exists(file_name):
                    os.remove(file_name)

            elif file_pickling == "2":  # for binary format pick class dictionary
                data_binary = binary_dict(file_name)
                print(type(data_binary)) # type class
                print("Contents of data:  \n ",(data_binary)) # print data
                if os.path.exists(file_name):
                    os.remove(file_name)
            
            elif file_type == "t":
                print("Contents of text file:")
                output_console(file_name)

        #Decrypt file if required
        if file_encrypted == "y":
            decrypt_file(file_name, output_type)

        clientsocket.close()
        print("\nClosing server")
        break

if __name__ == "__main__":
    main()
    
