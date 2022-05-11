import socket
import json
import os
import time


# Creating a socket.
host = input("Host Name: ")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Trying to connect to socket.
try:
    sock.connect((host, 22222))
    print("Connected Successfully")
except:
    print("Unable to connect")
    exit(0)



    """Function to recieve json file on server side"""
# Send json file details
file_name = sock.recv(100).decode('utf-8') # decode at server side (name)
file_size = sock.recv(100).decode('utf-8') # decode at server side (size)

# Opening and reading file
with open("./rec/" + file_name, "wb") as file:
    receive_size = 0
    # Starting the timer
    start_time = time.time()

    # Running the loop while file is fully recieved
while receive_size <= int(file_size):
    data = sock.recv(1024)
    if not (data):
        break
    file.write(data)
    receive_size += len(data)

    # Ending the timer
    end_time = time.time()

    print("File transfer Complete.Total time: ", end_time - start_time)

    # Closing the server side socket
    sock.close()
