#! /usr/bin/python
##################################################
#
# Realtime WLC Client Monitor
#
# Requires netmiko - sudo pip install netmiko
#
##################################################

from netmiko import ConnectHandler 
import getpass
import time

##################################################
#
# The fields we are parsing for in show output
#
##################################################

InterestingFields = {
    'Client MAC Address',
    'Client Username',
    'AP Name',
    'Client State',
    'Connected For',
    'Channel.',
    'IP Address',
    'Policy Type',
    'Encryption Cipher',
    'Radio Signal Strength Indicator',
    'Signal to Noise Ratio'
}

##################################################
#
# Function to refresh and print data
#
##################################################

def PrintClient(net_connect, strShowCommand):
    # Execute show and split into list
    output = net_connect.send_command(strShowCommand)
    lines = output.splitlines()

    print("\033c")

    for Field in InterestingFields:
        for line in lines:
            if line.strip().startswith(Field):
                print line
    time.sleep(1) 
    return;

##################################################
#
# Start of script
#
##################################################

strIPAddress = raw_input('Controller IP: ')
strUsername = raw_input('Username: ')
strPassword = getpass.getpass()
strMACAddress = raw_input('Client MAC Address: ')
strShowCommand = 'show client detail ' + strMACAddress

cisco_wlc = {
'device_type': 'cisco_wlc',
'ip': strIPAddress,
'username': strUsername,
'password': strPassword,
}


# Connect to the WLC
net_connect = ConnectHandler(**cisco_wlc)

# Loop until Control-C
try:
    while True:
        PrintClient(net_connect, strShowCommand)
except KeyboardInterrupt:
    pass

    
    