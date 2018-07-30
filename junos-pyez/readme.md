# Monitoring optical diagnostics for juniper devices
Python3 script used in nagios for monitoring tranciever parameters.

To install use:
```
pip install jxmlease
pip install argparse
pip install lxml
pip install junos-eznc
```
set up your junos device to use netconf:

```
set system login user netconf-access uid 2006
set system login user netconf-access class read-only
set system login user netconf-access authentication ssh-rsa "ssh-rsa PRIVATE KEY netconf@domain.local"

set system services netconf ssh
```
to test script run
 
```
python junos-optics-diagnostics.py netconf-access /path/to/privat/key 192.168.1.1 10
```
Output should be like
```
{'ge-0/0/0': {'bias': 'OK', 'rx-power': 'OK', 'voltage': 'OK'},
 'ge-0/0/1': {'bias': 'OK', 'rx-power': 'OK', 'voltage': 'OK'},
 'ge-0/0/2': {'bias': 'OK', 'rx-power': 'OK', 'voltage': 'OK'},
 'ge-0/0/3': {'bias': 'OK', 'rx-power': 'OK', 'voltage': 'OK'},
 'ge-0/0/4': {'bias': 'OK', 'rx-power': 'OK', 'voltage': 'OK'},
 'ge-0/1/0': {'bias': 'OK', 'rx-power': 'OK', 'voltage': 'OK'},
 'ge-0/1/1': {'bias': 'OK', 'rx-power': 'OK', 'voltage': 'OK'},
 'ge-0/1/2': {'bias': 'OK', 'rx-power': 'OK', 'voltage': 'OK'},
 'ge-0/1/3': {'bias': 'OK', 'rx-power': 'OK', 'voltage': 'OK'},
 'xe-2/0/0': {'bias': 'OK', 'rx-power': 'OK', 'voltage': 'OK'},
 'xe-2/0/1': {'bias': 'OK', 'rx-power': 'OK', 'voltage': 'OK'},
 'xe-2/0/2': {'bias': 'OK', 'rx-power': 'OK', 'voltage': 'OK'},
 'xe-2/0/3': {'bias': 'OK', 'rx-power': 'OK', 'voltage': 'OK'}}
 ```
 
 Add a command to nagios
 ```
 define command {
    command_name            junos_netconf_interfaces
    command_line            /usr/bin/python /opt/scripts/netconf/interfaces.py $ARG1$ $ARG2$ $HOSTADDRESS$ $ARG3$
}
```

Add a service:
```
define service{
    use                     generic-service
    host_name               MX;
    service_description     Optical diagnostics
    check_command           junos_netconf_interfaces!netconf-access!/path/to/private/key!10;
    normal_check_interval       10 ;
    retry_check_interval        3 ;
    contact_groups              admins;
    notification_interval       300
    notification_period         24x7
    notification_options        w,u,c,r
}
```
