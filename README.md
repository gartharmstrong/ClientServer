# ClientServer
# Program to send dictionary and text file to the server

## Short description
A simple client/server network to send dictionary and text file to the server locally. 

## Brief description
A client/server program comprises two modules:
1. The user can populate the dictionary, serialise it and send it to the server. The user can choose
one of the picking formats available.
* JSON
* Binary
* XML
2. The user can send text file to the server with an option available to encrypt the contents.


## Table of Contents
- [Install](#install)
- [Requirements](#requirements)
- [Usage](#usage)
- [Contribution](#contribution)
- [License](#license)

### Install
***
The virtual environment conda is used to develop a python code.
### Requirements
***
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the packages. Following python packages are required to execute the client-server program on the user machine.
1. To create a client-server communication with socket install the package [socket](https://pypi.org/project/sockets/) with ``` pip install sockets ```
2. To encrypt and decrypt the text file [Cryptography](https://cryptography.io/en/latest/fernet/) with ``` pip install cryptography ```
3. To JSON encoder/decoder and serialise/deserialise [JSON](https://docs.python.org/3/library/json.html#). json is a built-in module in python and does not need to install with pip.
4. To serialise/deserialise dictionary in binary using pickle module [Pickle](https://docs.python.org/3/library/pickle.html). The module can be installed by ``` pip install pickle-mixin ```
5. To handle the file operations install [shutil](https://docs.python.org/3/library/shutil.html) with ``` pip install shutil ```
6. To change dictionary to XML, parsing, string representation of XML install [elementpath](https://pypi.org/project/elementpath/) with ``` pip install elementpath ```
7. The modules ``` os, time, sys ``` are standard modules in python. 
8. On server side to convert XML to dictionary install [xmltodict](https://pypi.org/project/xmltodict/) with ``` pip install xmltodict ```

### Usage
***
In order to run the client-server program run the python files as instructed.
1. Run the server implementation with file "server.py" in the server folder at first and choose the required option. The message will appear on the terminal "Waiting for client to receive data" shows that server is ready for the client.
2. Run the client implementation with the file "client.py in the client folder and choose the required function with the interactive message displayed on the terminal.
> **_NOTE:_** 
1. The client-side will show an error to send data if the server is not initialised at first.
2. Run the python file "client.py" after changing the directory to the "client" folder. ``` ../client/python client.py ``` 
In other cases, the client program will be failed to find the text file when the user selects the "t" option.

``` File type: Text file(t) or Dictionary(d)? t ```

```Input is text file```

```textfile.txt does not exist. ```

**Expects**
* Based on the operators of the user, the function will be intialised and send the data to the server with the message "Completed sending data to server"

**Modifies**
* The functions pickled the data for the dictionary based on the chosen option and send to server. 
* For text file the function will send the data based on the option chosen by the user for encryption. The locked option will be displayed on the terminal after selection.    

**Output**
1. After successfully receiving the data. The message will appear "Received data" which shows the class of the object and received data. The session will be closed after successful receival. 

### Limitations / Exceptions
***
Exceptions are introduced in case user input wrong input where required.


### Contribution
***
This project for the public is available on https://github.com/gartharmstrong/ClientServer - Github [Github-ClientServer](https://github.com/gartharmstrong/ClientServer)
Group B: Garth Armstrong, Ghafer Ahmed Khan, Hasan Jadallah, Ho Him Lam

In order to write the code, some online tutorials are helpful. 
* For XML handling and parsing https://docs.python.org/3/library/xml.etree.elementtree.html – xml.etree.ElementTree — The ElementTree XML API [xml.etree.ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html)  
 

### License
***
MIT license  
A short and simple permissive license with conditions only requiring preservation of copyright and license notices. Licensed works, modifications, and larger works may be distributed under different terms and without source code.
