import socket                                  
from cryptography.fernet import Fernet
import os
import json
import pickle as pk
import xml.etree.ElementTree as et
import xmltodict

result_string = {}

def json_format(file_name): #function for json
    with open(file_name, 'r') as pkfile:
        unpickled = json.loads(pkfile.read())
    with open(file_name, 'w') as unpkfile:
        unpkfile.write(str(unpickled))

def json_dict(file_name): #function for json <class 'dict'>
    #For unittest only
    global result_string
    with open(file_name, 'r') as dictfile2:      
        result_string["Encoded_data"] =  dictfile2.read()

    with open(file_name, 'r') as dictfile:
        unpickled = json.loads(dictfile.read())
    return unpickled

def binary_format(file_name): #function for binary
    with open(file_name,'rb') as pkfile:
        unpickled = pk.load(pkfile)
    with open(file_name, 'w') as unpkfile:
        unpkfile.write(str(unpickled))
        
def binary_dict(file_name): #function for binary <class 'dict'>
    #For unittest only
    global result_string
    with open(file_name, 'rb') as pkfile2:      
        result_string["Encoded_data"] =  pkfile2.read()
        #print ("[Server] Encoded dictionary: ", result_string["Encoded_data"])
    
    #For production
    with open(file_name, 'rb') as pkfile:        
        unpickled = pk.load(pkfile, encoding='utf-8')
        return unpickled


def xml_format(file_name): # function for XML
    with open(file_name,'r') as pkfile: # added to code
        unpickled = et.parse(pkfile) # added to code
        root = unpickled.getroot()
        write_file = et.tostring(root)
        xml_decode = write_file.decode() 
        xml_datadict = xmltodict.parse(xml_decode) #change XML to dictionary
        xml_dict = dict(xml_datadict.pop('data'))
    with open(file_name, 'w',) as unpkfile: # added to code
        unpkfile.write(str(xml_dict)) # added to code

def xml_format_dict(file_name): # function for XML <class 'dict'>
    global result_string
    with open(file_name,'r') as pkfile: # added to code
        unpickled = et.parse(pkfile) # added to code
        root = unpickled.getroot()
        write_file = et.tostring(root)

        result_string["Encoded_data"] =  write_file #For unittest
        #print ("[Client] Encoded dictionary: ", result_string["Encoded_data"])

        xml_decode = write_file.decode() # 
        xml_datadict = xmltodict.parse(xml_decode) #change XML to dictionary
        xml_dict = dict(xml_datadict.pop('data'))
        return (xml_dict)

def decrypt_file(filename, output_type):
    global result_string
    key = open("key.key", "rb").read()
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    result_string["Encrypted"] = encrypted_data
    decrypted_data = f.decrypt(encrypted_data)
    if output_type == "c":
        print("\nDecrypted data: \n" + decrypted_data.decode("utf-8"))
    with open(filename, "wb") as file:
        file.write(decrypted_data)

def output_console(file_name):    
    with open(file_name,'r') as viewFileOpen:
        data = viewFileOpen.read()
    print(data)

def main(filetype):
    #for unittest
    global result_string

    # create a socket object
    serversocket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    if not filetype:
        host = socket.gethostname()
    else:
        host = '0.0.0.0'
    port = 29999
    # bind to the port
    try:
        serversocket.bind((host, port))
        print("Socket bind successful")
    except:
        print("Unable to bind socket")
        exit(0)
    
    if not filetype:
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
    else:
        output_type = filetype
    
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

        if not filetype:
            print("[Server] \nFile type: " + file_type)
            print("[Server] Pickling: " + file_pickling)
            print("[Server] File encrypted: " + file_encrypted)
            print("[Server] Filename: " + file_name)
        
        if filetype:
            file_name = os.path.join("server", file_name)
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
                xml_format(file_name)
            print("File written to server")
        
        elif output_type.lower() == 'c':
            # User choose to print on console
            if file_pickling == "1": # for json format pick class dictionary
                data_json = json_dict(file_name)                
                with open(file_name, 'r') as f:
                    c = f.read()
                if not filetype:
                    print(type(data_json))
                    print("Contents of data: \n{}".format(c))  
                else:
                    result_string["Unencrypted"] = format(c)

                if os.path.exists(file_name):
                    os.remove(file_name)

            elif file_pickling == "2":  # for binary format pick class dictionary
                data_binary = binary_dict(file_name)
                if not filetype:
                    print(type(data_binary)) # type class
                    print("Contents of data:  \n ",data_binary) # print data                      
                else:
                    result_string["Unencrypted"] = data_binary
                    #print("[Server] test result string 1: ", result_string["Unencrypted"] ) 

                if os.path.exists(file_name):
                    os.remove(file_name)
            elif file_pickling == "3":  # for xml format pick class dictionary
                xml_file = xml_format_dict(file_name)
                if not filetype:
                    print(type(xml_file)) # type class
                    print("Contents of data:  \n ",xml_file) # print data
                else:
                    result_string["Unencrypted"] = xml_file
                    #print("[Server] test result string 1: ", result_string["Unencrypted"] ) 

                if os.path.exists(file_name):
                    os.remove(file_name)
            elif file_type == "t":
                if not filetype:
                    print("Contents of text file:")
                    output_console(file_name)
                else:
                    result_string["Unencrypted"] = file_name
                    #print("[Server] test result string 1: ", result_string )                

        #Decrypt file if required
        if file_encrypted == "y":
            decrypt_file(file_name, output_type)
        if file_type == "t" and output_type == "c" and not filetype:
            os.remove(file_name)

        clientsocket.close()
        print("\nClosing server")
        break
    #print("[Server] test result string 2: ", result_string )
    return result_string

if __name__ == "__main__":
    main("")
