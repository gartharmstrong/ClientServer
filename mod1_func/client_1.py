import socket
import json
import os
import time

client = None 
# Module for client 
# Creating a socket.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((socket.gethostname(), 22222))
sock.listen(5)
print("Host Name: ", sock.getsockname())

# Accepting the connection.
client, addr = sock.accept()

# Contents of dicitonary
dict = {
    'name' : 'Ghafer',
    'Age' : 21,
    'Occupation' : 'Engineer'
}


"""Function to write data into json file"""
j = json.dumps(dict)
with open('mydata.json', 'w') as f:
    f.write(j)
    print("Dictionary created successfully")


# Getting file details
def file_send():
    """Function to send json file"""
    file_name = input("mydata.json")
    file_size = os.path.getsize(file_name) #determine the file size to send
    # Sending file_name and detail.
    client.send(file_name.encode('utf-8'))
    client.send(str(file_size).encode('utf-8'))

# Opening file and sending data.
    with open(file_name, "rb") as file:
        recv_size = 0
    # Starting the time capture.
    start_time = time.time()

    # Running loop while c not equals to file_size.
    while recv_size <= file_size:
        data = file.read(1024)
        if not (data):
            break
        client.sendall(data)
        recv_size += len(data)
        print ("File sent: %s" % len(data))
    print("File transferred %s successfully..." % file_size)

    # Ending the time capture.
    end_time = time.time()
    print ("File Transfer Complete.Total time: ", end_time - start_time)
f.close()
client.close()
