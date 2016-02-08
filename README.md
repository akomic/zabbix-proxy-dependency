# zabbix-proxy-dependency

This program takes as required input zabbix hostname and returns the health status of the zabbix proxy if the host is using one.
If there is no proxy for the specified host, 1 (available) is going to be returned.
Idea is to have something the host can depend on if the zabbix proxy goes down in order to avoid avalanche of alerts.
For this to work, you need to have zabbix agent installed on the zabbix proxy machine and added as regular host for monitoring.

Tested with Zabbix 2.2

## Installation

pyzabbix is required
```
$ pip install pyzabbix
```

Download to zabbix server
``` 
$ git clone https://github.com/akomic/zabbix-proxy-dependency
$ cd zabbix-proxy-dependency
```

Copy script to directory specified in zabbix_server.conf file as ExternalScript=
```
$ cp zabbix_check.py /etc/zabbix/externalscripts/
$ chmod 755 /etc/zabbix/externalscripts/zabbix_check.py
```

### Configuration

- Create user with read-only privileges for hosts that are going to use this script.

- Import template zbx_export_templates.xml

- Edit macros for the template and specify apihost ({$ZABBIX_API}) as URL on which we can communicate with zabbix frontend, username and password of previously created user as {$ZABBIX_USER} and {$ZABBIX_PASS}

- Add template to host that is receiving data through zabbix proxy.

Template is adding item which is indicating availability status of the zabbix proxy that monitored host is using.
If the zabbix proxy on which is monitored host is depending is not available, item is going to have value of 0. If everything is ok item is going to have value of 1.

- Use added item in creation of active checks to skip sending alerts

or

- Use added item as dependency for hosts availability trigger e.g. Zabbix agent on {HOST.NAME} is unreachable for 5 minutes" in "Template OS Linux"
