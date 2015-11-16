Installling SDNCLI

Development Environment


1. Install PIP

    On Ubuntu:  

    1. sudp apt-get update
    2. sudo apt-get install git python-pip
    3. sudo pip install virtualenv

2. Setup VirtualEnv

    1. mkdir working 
    2. cd working
    3. virtualenv sdn
    4. source sdn/bin/activate
    5. git clone https://github.com/gaberger/pybvc
    6. git clone https://github.com/gaberger/sdncli.git
    6. cd pybvc
    7. pip install -r requirements
    8. python setup.py developers
    9. cd ../sdncli
    10. pip install -r requirements
    11. python setup.py develop

3. Setup Controller Address  
    1. export BSCADDR=<controllerIP>

4. Check ConnectionError

    1. sdncli show nodes

5. Mount Netconf Device

    1. sdncli node mount <name> <address> <user> <password>
