import socket
from cryptography.fernet import Fernet
import json
from xml.etree.ElementTree import Element, tostring # added to code
import pickle as pk
import time

# Dictionary 
data = {
    'Group': 'B',
    'Program':'Client Server', 
    'Task':'Send dictionary'
}

json_pick = json.dumps(data) # for pickling JSON format 
binary_pick = pk.dumps(data) # for picking binary format

xml_pick = Element('data') # to change the data dictionary to an xml file (added to code)
for key, value in data.items(): # changing the data into keys and values (added to code)
    child_node = Element(key) # added to code
    child_node.text = value # added to code
    xml_pick.append(child_node) # added to code

def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def encrypt_file(filename):
    key = open("key.key", "rb").read()
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)

def main():
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
            msg_pickling = input("1, A\n"
                    "2, B\n"
                    "3, C\n"
                    "Choose 1 for JSON, 2 for Binary format, 3 for XML :")
            if (str(msg_pickling) == "1"):
                sendmesg = str.encode(json_pick) # pick for JSON format
                break
            elif (str(msg_pickling) == "2"):
                sendmesg = binary_pick # pick for binary format
                break
            elif (str(msg_pickling) == "3"):
                sendmesg = tostring(xml_pick) # pick for XML format (added to code)
                break
            else:
                print("invalid selection")
    else:
        msg_pickling="0" #default value if text file

    #File encryption - only for text file
    if file_type == "t":
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
        file_encrypted="n" #default value if dictionary

    #File name
    while True:
        file_name = input("Enter filename to be sent: ")
        break
    
    #Encrypt file if required
    if file_encrypted == "y":
        encrypt_file(file_name)

    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    # get local machine name
    host = socket.gethostname()                           

    port = 29955

    # connection to hostname on the port.
    s.connect((host, port))                               
    print("Connected")

    s.send(file_type.encode('utf-8'))
    s.send(msg_pickling.encode('utf-8'))
    s.send(file_encrypted.encode('utf-8'))
    s.send(file_name.encode('utf-8'))

    if file_type == "t":
        file = open(file_name,'rb')
        data = file.read(1024)
        while (data):
            s.send(data)
            data = file.read(1024)
        file.close()
    elif file_type == "d":
        time.sleep(2)
        print("Pickled data: " + str(sendmesg))
        s.send(sendmesg)

    s.close()

    print("Completed sending data to server")

if __name__ == "__main__":
    main()
