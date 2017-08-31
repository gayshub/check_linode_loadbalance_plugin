#!/usr/bin/python

import requests
import time
import sys
from subprocess import call

iplist = ['LB_IP1', 'LB_IP2']
domain = sys.argv[1]

def Delhost(ip):
    if ip in open('/etc/hosts').read():
        with open('/etc/hosts','r') as source:
            lines = source.readlines()
        with open('/etc/hosts','w') as source:
            for line in lines:
                if ip not in line:
                    source.write(line)


def Addhost(ip):
    if ip not in open('/etc/hosts').read():
        with open('/etc/hosts','a') as source:
            source.write(i + '   ' + domain + '\n')

def Checkweb(ip,timeout=10):
    for j in range(2):
        r = requests.get('https://' + 'accout:passowrd' + ip + '/Stats', verify=False, timeout=timeout)
        print r.text
        if r.status_code != 200:
            print "The status code is not 200"
            if j == 1:
                try:
                    Delhost(ip)
                    call(["/etc/init.d/dns-clean", "start"])
                except:
                    break
            time.sleep(20)
        else:
            Addhost(ip)
            

for i in iplist:
    try:
        Checkweb(i)
    except requests.exceptions.HTTPError:
        Checkweb(i)
    except requests.exceptions.Timeout:
        Delhost(i)

