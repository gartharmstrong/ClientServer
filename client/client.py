from argparse import FileType
import socket
from cryptography.fernet import Fernet
import json
import pickle as pk
import time
import shutil
import os
import sys
from xml.etree.ElementTree import Element, tostring

# Dictionary 
data = {
    'Group': 'B',
    'Program':'Client Server', 
    'Task':'Send dictionary'
}

file_type = ""
msg_pickling = ""
sendmesg = ""
file_name = ""
file_encrypted = ""
result_string = {}

json_pick = json.dumps(data) # for pickling JSON format 
binary_pick = pk.dumps(data) # for picking binary format
xml_pick = Element('data') # to change the data dictionary to an xml file
for key, value in data.items(): # changing the data into keys and values
    child_node = Element(key)
    child_node.text = value
    xml_pick.append(child_node)

def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def encrypt_file(filename):
    global result_string
    key = open("key.key", "rb").read()
    f = Fernet(key)
    dest = filename + "backup"
    shutil.copy(filename, dest)
    with open(filename, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)
    result_string["Encrypted"] = encrypted_data
    print("Encrypted result: ", result_string["Encrypted"])

def main(type, format, encrypted):
    
    def inputs():
        global file_type 
        global msg_pickling 
        global sendmesg 
        global file_name
        global file_encrypted
        
        #File type
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

        #File Pickling - only for dictionary
        if file_type == "d":
            while True:
                msg_pickling = print(f"Choose pickling format")
                msg_pickling = input("1, JSON\n"
                        "2, Binary\n"
                        "3, XML\n"
                        "Choose 1 for JSON, 2 for Binary format, 3 for XML : ")
                if (str(msg_pickling) == "1"):
                    file_name = "jsonfile.txt"
                    sendmesg = str.encode(json_pick) # pick for JSON format
                    break
                elif (str(msg_pickling) == "2"):
                    file_name = "binaryfile.txt"
                    sendmesg = binary_pick # pick for binary format
                    break
                elif (str(msg_pickling) == "3"):
                    file_name = "xmlfile.txt"
                    sendmesg = tostring(xml_pick) # pick for XML format
                    break
                else:
                    print("invalid selection")
        else:
            msg_pickling="0" #default value if text file

        #File encryption - only for text file
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
            file_encrypted="n" #default value if dictionary
        
        #Encrypt file if required
        if file_encrypted == "y":
            encrypt_file(file_name)

    if type == "":
        inputs()
    else:
        global file_type 
        global msg_pickling 
        global sendmesg 
        global file_name
        global file_encrypted

        file_type = type
        msg_pickling = format   
        if file_type == "d":
            if (str(msg_pickling) == "1"):
                file_name = "jsonfile.txt"
                result_string["Unencrypted"] = json.dumps(data)
                sendmesg = str.encode(json_pick) # pick for JSON format
                result_string["Encoded_data"] = sendmesg
                
            elif (str(msg_pickling) == "2"):
                file_name = "binaryfile.txt"
                result_string["Unencrypted"] = data
                sendmesg = pk.dumps(data) # pick for binary format
                result_string["Encoded_data"] = sendmesg
                
            elif (str(msg_pickling) == "3"):
                file_name = "xmlfile.txt"
                result_string["Unencrypted"] = data
                sendmesg = tostring(xml_pick) # pick for XML format
                result_string["Encoded_data"] = sendmesg
        
        if file_type == "t":
            file_name = "textfile.txt"
            print("[Test] file path: ", file_name)
                    
        file_encrypted = encrypted
        if file_encrypted == "y":
            encrypt_file(file_name)

    if not type:
        print("[Client] File type: " + file_type)
        print("[Client] Msg pickling: " + msg_pickling)
        print("[Client] Filename: " + file_name)
        print("[Client] File encrypted?: " + file_encrypted)

    def socketSetUp():
        global result_string
        # create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

        # get local machine name
        host = socket.gethostname()
        port = 29999

        # connection to hostname on the port.
        s.connect((host, port))                               
        print("Connected to server")

        s.send(file_type.encode('utf-8'))
        s.send(msg_pickling.encode('utf-8'))
        s.send(file_encrypted.encode('utf-8'))
        s.send(file_name.encode('utf-8'))

        time.sleep(2)

        if file_type == "t":
            file = open(file_name,'rb')
            data = file.read(1024)
            result_string["Unencrypted"] = file_name
            while (data):
                s.send(data)
                data = file.read(1024)
                print(data)
                
            file.close()
        elif file_type == "d":            
            s.send(sendmesg)
            if not type:
                print("Pickled data: " + str(sendmesg))

        if file_encrypted == "y":
            backup = file_name + "backup"
            shutil.copy(backup, file_name)
            os.remove(backup)

        s.close()

        print("Completed sending data to server")
    socketSetUp()
    return result_string

if __name__ == "__main__":
    main("","","")
