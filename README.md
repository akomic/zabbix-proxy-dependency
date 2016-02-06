# zabbix-proxy-dependency

This program takes as required input zabbix hostid and returns the health status of the zabbix proxy if the host is using one.
If there is no proxy for the specified host, 1 (available) is going to be returned.
Idea is to have something the host can depend on if the zabbix proxy goes down in order to avoid avalanche of alerts.
For this to work, you need to have zabbix agent installed on the zabbix proxy machine and added as regular host for monitoring.

