#!/usr/bin/python

"""
This program takes as required input zabbix hostname and returns the health status of the zabbix proxy if the host is using it.
If there is no proxy for the specified host, 1 (available) is going to be returned.
Idea is to have something the host can depend on if the zabbix proxy goes down in order to avoid avalanche of alerts.
For this to work, you need to have zabbix agent installed on the zabbix proxy machine and zabbix proxy machine added as regular host for monitoring.
"""

__author__ = "Alen Komic"
__license__ = "GPL"
__version__ = "1.0"

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--hostname",help="Host Name as defined in zabbix", required=True)
parser.add_argument("--apihost",help="Zabbix API URL")
parser.add_argument("--username",help="Zabbix Username")
parser.add_argument("--password",help="Zabbix Password")
parser.add_argument("--verbose",help="Up the verbosity, for debugging purposes", action="count")
args = parser.parse_args()

import os
import sys
import pyzabbix
import requests


zuser = ( args.username or os.getenv('ZABBIX_USER') )
zpass = ( args.password or os.getenv('ZABBIX_PASS') )
apihost = ( args.apihost or os.getenv('ZABBIX_API') )

if not zuser or not zpass:
  print "You must specify zabbix apihost, username, password via cli or ENV"
  sys.exit(1)
try:
  zapi = pyzabbix.ZabbixAPI(apihost)

  zapi.login(zuser,zpass)
  if args.verbose:
    print "Connected to Zabbix API Version %s" % zapi.api_version()

  # Default is to return 1 (available), even if zabbix proxy does not exist for the specified host.
  proxy_dep_alive=1

  # Looking for host with given hostname
  for host in zapi.host.get(filter={"host": args.hostname}, output="extend", limit=1):
    if args.verbose:
      print "Checking host name:",args.hostname,"host id:",host['hostid']
    # Is there zabbix proxy this host is using?
    if host['proxy_hostid']:
      # Getting the proxy hostname
      for proxy in zapi.proxy.get(proxyids=[host['proxy_hostid']], output="extend", limit=1):
        if args.verbose:
          print "Proxy id:",proxy['proxyid'],"proxy host:",proxy['host']

        # Zabbix proxy is represented as regular host, we are counting on it.
        for proxyhost in zapi.host.get(filter={"host": proxy['host']}, output="extend", limit=1):
          if not proxyhost.get('available'):
            proxy_dep_alive=0
  if args.verbose:
    print "Proxy availability status:",
  print proxy_dep_alive

except requests.exceptions.HTTPError as e:
  print "ERROR login to zabbix API:", str(e)
except pyzabbix.ZabbixAPIException as e:
  print "API Error:", str(e)
except Exception as e:
  print "ERROR: %s" % str(e)

