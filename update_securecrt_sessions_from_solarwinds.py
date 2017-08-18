# $language = "Python"
# $interface = "1.0"

#**************************************************************************
#
# This script syncs all nodes from Solarwinds into securecrt as sessions 
#
# Prior to using this script you must:
# - Install XCode from the app store
# - Install PIP from terminal: sudo easy_install pip
# - Install orionsdk from pip: sudo pip install orionsdk
#
#**************************************************************************

# Read only user needed for API
strSolarwindsHost = "solarwinds.company.com"
strSolarwindsUser = "swuser"
strSolarwindsPassword = "swpass"

import orionsdk
import json
import datetime
import os
import platform
import re
import shutil
import sys
import time
import subprocess

# Establish API Connection
swis = orionsdk.SwisClient(strSolarwindsHost, strSolarwindsUser, strSolarwindsPassword)

# Query for Nodes, group membership and NCM properties
results = swis.query("SELECT containermembers.MemberPrimaryID AS primary_id,containermembers.DisplayName AS display_name,containermembers.ContainerID AS container_id,containermembers.MemberEntityType AS member_entity_type,  container.DisplayName as container_name, ncmnode.ConnectionProfile as connection_profile, ncmnode.DeviceTemplate as template, orionnode.IPAddress as ip_address FROM Orion.ContainerMembers containermembers LEFT JOIN NCM.NodeProperties ncmnode ON containermembers.MemberPrimaryID=ncmnode.CoreNodeID LEFT JOIN Orion.Container container ON containermembers.ContainerID=container.ContainerID LEFT JOIN Orion.Nodes orionnode ON containermembers.MemberPrimaryID=orionnode.NodeID WHERE member_entity_type='Orion.Nodes'")

for result in results['results']:
    
    crt.Session.SetStatusText(result['display_name'])
    
    # Identify TELNET or SSH
    if result['connection_profile'] == 6:
        strProtocol = "TELNET"
        strPort = "23"
    else:
        strProtocol = "SSH2"
        strPort = "22"
    
    # Set variables for session based on JSON from OrionSDK
    strDisplayName = result['display_name']
    strFolder = result['container_name']
    strIPAddress = result['ip_address']
    strSessionPath = strFolder + "/" + strDisplayName
    
    # Build a session using global defaults
    objConfig = crt.OpenSessionConfiguration("Default")
    objConfig.Save(strSessionPath)
    objConfig = crt.OpenSessionConfiguration(strSessionPath)
    
    # Overwrite default values we care about and save session
    objConfig.SetOption("Hostname", strIPAddress)
    objConfig.SetOption("Protocol Name", strProtocol)
    objConfig.Save()

# Update session managers display    
crt.Sleep(2000)
crt.Session.SetStatusText("")    