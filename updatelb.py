#!/usr/bin/python
import requests
import time
import re
import sys
import os

ZONEID = sys.argv[1]
KEY = sys.argv[2]
EMAIL = sys.argv[3]
baseurl = "https://api.cloudflare.com/client/v4/zones/"
url = baseurl + ZONEID + '/dns_records'
headers = {'Content-Type':'application/json', 'X-Auth-Key': KEY, 'X-Auth-Email': EMAIL}
DOMAIN = sys.argv[4]


def getIPCount(domain):
    r = requests.get(url + '?', headers=headers, params={'type': 'A', 'name': domain }) 
    return r.json()['result_info']['total_count']

def GetIPID(content):
    r = requests.get(url + '?', headers=headers, params={'type': 'A', 'name': DOMAIN, 'content': content}) 
    return r.json()['result'][0]['id']

def CreateDNS(ip):
    r = requests.post(url, headers=headers, json={'type': 'A', 'name': DOMAIN, 'content': ip})
    return r.text

def DelDNS(ip):
    r = requests.request('DELETE', url + '/' + GetIPID(ip), headers=headers)
    print r.text

def Checkweb(ip,timeout=5):
    for j in range(3):
        r = requests.get('https://' + 'accout:password' + ip + '/Stats', verify=False, timeout=timeout)
        if r.status_code != 200:
            print "The status code is not 200"
            if j == 2:
                try:
		    if getIPCount(DOMAIN) <= 1:
                        break
                    DelDNS(ip)
                except:
                    break
            print j
            time.sleep(20)
        else:
            try:
                result = GetIPID(ip)
		if result is not None:
			break
                print "getipid"
            except:
                CreateDNS(ip)               
                print "creating ip to cf"
                time.sleep(1)
                break
            else:
                print "The DNS resolve create donesn't work and maybe the items is exist"
    

def Checkwebsite():
    f = open('/tmp/updatedns_lock_{{ SITE }}','a') 
    iplist = [ 'LB_IP1', 'LB_IP2' ]  #loadbalance ip list
    for i in iplist:  
        try:
            Checkweb(i)
        except requests.exceptions.Timeout:
            print "Connection Timeout"
            Checkweb(i,10)
        except requests.exceptions.HTTPError:
            print "HTTP Response Error"
            Checkweb(i)
    os.remove('/tmp/updatedns_lock')

Checkwebsite()
