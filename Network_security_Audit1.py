import os
import sys
import subprocess
import time
import re
import getpass
import argparse
import string
from pprint import pprint
from threading import Thread
import paramiko
from multiprocessing import Pool

output=""
print "Enter the filename with hosts"
flname = raw_input()
f=open(flname,'r')
username=getpass.getuser()
password=getpass.getpass()
cisco_file = open('cisco.txt','a')
juniper_file = open('juniper.txt','a')
for line in f:
        print line
        variable = os.popen('host '+line).read()
        #print variable
        s = variable.split(" ")
        try:
            remote_conn_pre = paramiko.SSHClient()
            remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            remote_conn_pre.connect(line.strip(), port = 22, username=username, password= password, look_for_keys=False,allow_agent=False, timeout=30)
            channel = remote_conn_pre.invoke_shell()
        except Exception as e:
            print "Invalid SSH credentials.Press Ctrl C to exit."
        commands = ['sh run | i ACL-VTY-NETOPS-V6\n', 'show configuration protocols bgp | display set | match EBGP-TRANSIT-CONT | match prefix-limit\n']
        output = "" 
        if "bbr" in line or "crt" in line:
            channel.send("\n")
            time.sleep(1)
            channel.send(commands[1])
            time.sleep(2)
            output += channel.recv(5000000)
            if "prefix-limit maximum 700000" in output or "prefix-limit maximum 800000" in output:
                juniper_file.write(line+"prefix limit is configured on perring session")
                print "prefix limit is configured on perring session"
            else:
                juniper_file.write(line+"prefix limit is not configured on perring session")
                print "prefix limit is not configured on perring session"
        else:
            channel.send("\n")
            time.sleep(1)
            channel.send(commands[0])
            time.sleep(2)
            output += channel.recv(5000000)
            if "ACL-VTY-NETOPS-V6" in output:
                cisco_file.write(line+"ACL-VTY-NETOPS-V6 acl is configured on the device\n")
                print "ACL-VTY-NETOPS-V6 acl is configured on the device"
            else:
                cisco_file.write(line+"ACL-VTY-NETOPS-V6 acl is missing on the device\n")
                print "ACL-VTY-NETOPS-V6 acl is missing on the device"
cisco_file.close()
juniper_file.close()