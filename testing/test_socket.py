import os
from unittest import result
import warnings
from server.server import main as server
from client.client import main as client, encrypt_file as encrypt, data as data_set

import unittest
import sys
import socket
import threading

stream_lock = threading.Lock()
sentData = {}        
receivedData = {}

class TestSocket(unittest.TestCase):
    print("Start testing")

    def runTest(self):
        global sentData      
        global receivedData 
      
        def server_func(self, readMethod, filetype, encrypted):    
            result = server(readMethod)
            #print("Server result: ",result)
            stream_lock.acquire()
            try:
                result["Unencrypted"] = result["Unencrypted"].decode('UTF-8')
                #print("Converting server result to string")
            except (UnicodeDecodeError, AttributeError):
                #print("Server result is a string")
                pass
            #print("Type of server result: ",type(result["Unencrypted"]))
            receivedData["Data"] = result["Unencrypted"]
            if encrypted == "y":
                receivedData["Encrypted_Data"] = result["Encrypted"] 
                #print("Server encrypted data: ",receivedData["Encrypted_Data"])
            if filetype == "d":                
                receivedData["Encoded_Data"] = result["Encoded_data"] 
                try:
                    receivedData["Encoded_Data"] = receivedData["Encoded_Data"].decode('UTF-8')
                    #print("Converting encoded server result to string")
                except (UnicodeDecodeError, AttributeError):
                    #print("Server encoded result is a string")
                    pass
            #print("Saved server result - ",receivedData)
            stream_lock.release() 

        def client_func(self, filetype, format, encrypted):
            result = client(filetype, format, encrypted)
            #print("Client result: ",result)
            stream_lock.acquire()
            try:
                result["Unencrypted"] = result["Unencrypted"].decode('UTF-8')
                #print("Converting client result to string")
            except (UnicodeDecodeError, AttributeError):
                #print("Client result is a string")
                pass

            #print("Type of client result: ",type(result["Unencrypted"]))
            sentData["Data"] = result["Unencrypted"]
            if encrypted == "y":
                sentData["Encrypted_Data"] = result["Encrypted"]
            if filetype == "d":                
                sentData["Encoded_Data"] = result["Encoded_data"] 
                try:
                    sentData["Encoded_Data"] = sentData["Encoded_Data"].decode('UTF-8')
                    #print("Converting client encoded result to string")
                except (UnicodeDecodeError, AttributeError):
                    #print("Client encoded result is a string")
                    pass
            #print("Saved client result - ",sentData)
            stream_lock.release()            

        #test sending unencrypted file
        def test_sendfile_u(self):
            print("\n===========================================\nTest for sending unencrypted file\n===========================================\n")
            t_server = threading.Thread(target=server_func, args=(self, "c", "t", "n"))        
            t_client = threading.Thread(target=client_func, args=(self, "t", "0", "n"))
            
            t_server.start()
            t_client.start()      
            warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)      
            t_server.join()
            t_client.join()            
            
            fileDir = os.path.dirname(os.path.realpath('__file__'))

            #read client sent data
            global sentData
            #print("Print path: ", sentData["Data"])
            file_name = os.path.join("client",sentData["Data"])
            sentData["Data"] = os.path.join(fileDir, file_name)
            file = open(sentData["Data"],'rb')
            data = file.read(1024)
            sentData["Result"] = data
            #print("Client sent data: ",data)

            #read server received data
            global receivedData
            #print("Print server path: ", receivedData["Data"])
            receivedData["Data"] = os.path.join(fileDir, receivedData["Data"])
            file = open(receivedData["Data"],'rb')
            data = file.read(1024)
            receivedData["Result"] = data
            #print("Sever received data: ",data)                

            print("Sent Data:", sentData)
            print("Received Data:", receivedData)
            self.assertEqual(sentData["Result"], receivedData["Result"],
                                    "Unencrypted file content is incorrect")

            sentData = {}
            receivedData = {}
        
        #test sending encrypted file
        def test_sendfile_e(self):
            print("\n===========================================\nTest for sending encrypted file\n===========================================\n")
            t_server = threading.Thread(target=server_func, args=(self, "c", "t", "y"))        
            t_client = threading.Thread(target=client_func, args=(self, "t", "0", "y"))
            
            t_server.start()
            t_client.start()      
            warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)      
            t_server.join()
            t_client.join()             
            
            fileDir = os.path.dirname(os.path.realpath('__file__'))

            #read client sent data
            global sentData
            #print("Print path: ", sentData["Data"])
            file_name = os.path.join("client",sentData["Data"])
            sentData["Data"] = os.path.join(fileDir, file_name)
            file = open(sentData["Data"],'rb')
            data = file.read(1024)
            sentData["Result"] = data
            #print("Client sent data: ",data)

            #read server received data
            global receivedData
            #print("Print server path: ", receivedData["Data"])
            receivedData["Data"] = os.path.join(fileDir, receivedData["Data"])
            file = open(receivedData["Data"],'rb')
            data = file.read(1024)
            receivedData["Result"] = data
            #print("Sever received data: ",data)              
            
            print("Sent Data:", sentData)
            print("Received Data:", receivedData)
            self.assertEqual(sentData["Encrypted_Data"], receivedData["Encrypted_Data"],
                                    "Encrypted file data is incorrect")
            self.assertEqual(sentData["Result"], receivedData["Result"],
                                    "Encrypted file content is incorrect")

            sentData = {}
            receivedData = {}

        #test sending dictionary in json
        def test_json(self):
            print("\n===========================================\nTest for sending dictionary in json\n===========================================\n")
            t_server = threading.Thread(target=server_func, args=(self, "c", "d", "n"))        
            t_client = threading.Thread(target=client_func, args=(self, "d", "1", "n"))
            
            t_server.start()
            t_client.start()      
            warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)      
            t_server.join()
            t_client.join()              

            global sentData
            global receivedData        
            
            print("Sent Data:", sentData)
            print("Received Data:", receivedData)
            
            self.assertEqual(sentData["Encoded_Data"], receivedData["Encoded_Data"],
                                    "Json encoded dictionary is incorrect")
            self.assertEqual(sentData["Data"], receivedData["Data"],
                                    "Json dictionary is incorrect")

            sentData = {}
            receivedData = {}

        #test sending dictionary in binary
        def test_binary(self):
            print("\n===========================================\nTest for sending dictionary in binary\n===========================================\n")
            t_server = threading.Thread(target=server_func, args=(self, "c", "d", "n"))        
            t_client = threading.Thread(target=client_func, args=(self, "d", "2", "n"))
            
            t_server.start()
            t_client.start()      
            warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)      
            t_server.join()
            t_client.join()              

            global sentData
            global receivedData        
            
            print("Sent Data:", sentData)
            print("Received Data:", receivedData)
            
            self.assertEqual(sentData["Encoded_Data"], receivedData["Encoded_Data"],
                                    "Binary encoded dictionary is incorrect")
            self.assertEqual(sentData["Data"], receivedData["Data"],
                                    "Binary dictionary is incorrect")

            sentData = {}
            receivedData = {}
        
        #test sending dictionary in xml
        def test_xml(self):
            print("\n===========================================\nTest for sending dictionary in xml\n===========================================\n")
            t_server = threading.Thread(target=server_func, args=(self, "c", "d", "n"))        
            t_client = threading.Thread(target=client_func, args=(self, "d", "3", "n"))
            
            t_server.start()
            t_client.start()      
            warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)      
            t_server.join()
            t_client.join()              

            global sentData
            global receivedData        
            
            print("Sent Data:", sentData)
            print("Received Data:", receivedData)
            
            self.assertEqual(sentData["Encoded_Data"], receivedData["Encoded_Data"],
                                    "Xml encoded dictionary is incorrect")
            self.assertEqual(sentData["Data"], receivedData["Data"],
                                    "Xml dictionary is incorrect")

            sentData = {}
            receivedData = {}

        test_sendfile_u(self)
        test_sendfile_e(self)
        test_json(self)
        test_binary(self)
        test_xml(self)

if __name__ == '__main__':    
    unittest.main(argv=['first-arg-is-ignored'], exit=False)