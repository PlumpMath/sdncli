
# sdncli [![Build Status](https://travis-ci.org/gaberger/sdncli.svg)](https://travis-ci.org/gaberger/sdncli)
Python Application to interface with Brocade SDN Controller
=======
## Installation

Development Environment

###Install PIP

    On Ubuntu:  

    ```bash 
    sudp apt-get update
    sudo apt-get install git python-pip
    sudo pip install virtualenv
    ```

###Setup VirtualEnv

   ```bash
   mkdir working 
   cd working
   virtualenv sdn
   source sdn/bin/activate
   git clone https://github.com/gaberger/sdncli.git
   cd ../sdncli
   python setup.py develop
   ```

###Setup Controller Address  

    ```bash
    export BSCADDR=<controllerIP>
    ```

###Check ConnectionError

    ```bash 
    sdncli show nodes
    ```

###Mount Netconf Device
    
    ```bash 
    sdncli node mount <name> <address> <user> <password>
    ```