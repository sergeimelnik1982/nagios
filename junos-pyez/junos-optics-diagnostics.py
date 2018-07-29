__author__ = 'sergeimelnik1982'
__version__= 0.1

from jnpr.junos import Device
import jnpr.junos.exception
from pprint import pprint
from lxml import etree
import jxmlease
import argparse
import re

parser = argparse.ArgumentParser(description='Get information on optical trancievers', usage='host user key timeout' )
parser.add_argument('user', help='username')
parser.add_argument('key', help='full path to rsa private key')
parser.add_argument('host', help='set host address')
parser.add_argument('timeout', help='set host timeout')

args = parser.parse_args()

dev = Device(host=args.host, user=args.user, ssh_private_key_file=args.key, gather_facts=False)
dev.open()
subs_info=dev.rpc.get_interface_optics_diagnostics_information()
xmlroot = jxmlease.parse(etree.tostring(subs_info, encoding='unicode'))
interface_data = xmlroot['interface-information']['physical-interface']
result = {}
exitcode = 0
for interface in interface_data:
    result[interface['name'].get_cdata()] = {}
    if re.search('[a-zA-Z]', interface['optics-diagnostics']['laser-rx-power-low-alarm-threshold-dbm']):
        result[interface['name']]['ddm_status'] = 'BAD DDM'
    else:
        if float(interface['optics-diagnostics']['laser-bias-current-low-alarm-threshold']) >= float(interface['optics-diagnostics']['laser-bias-current']):
            result[interface['name']]['bias'] = 'Low alarm'
            exitcode = 2
        elif float(interface['optics-diagnostics']['laser-bias-current']) >= float(interface['optics-diagnostics']['laser-bias-current-high-alarm-threshold']):
            result[interface['name']]['bias'] = 'High alarm'
            exitcode = 2
        elif float(interface['optics-diagnostics']['laser-bias-current-low-warn-threshold']) >= float(interface['optics-diagnostics']['laser-bias-current']):
            result[interface['name']]['bias'] = 'Low warn'
            if exitcode != 2:
                exitcode = 1
        elif float(interface['optics-diagnostics']['laser-bias-current-high-warn-threshold']) <= float(interface['optics-diagnostics']['laser-bias-current']):
            result[interface['name']]['bias'] = 'High warn'
            if exitcode != 2:
                exitcode = 1
        else:
            result[interface['name']]['bias'] = 'OK'

        if float(interface['optics-diagnostics']['module-voltage-low-alarm-threshold']) >= float(interface['optics-diagnostics']['module-voltage']):
            result[interface['name']]['voltage'] = 'Low alarm'
            exitcode = 2
        elif float(interface['optics-diagnostics']['module-voltage']) >= float(interface['optics-diagnostics']['module-voltage-high-alarm-threshold']):
            result[interface['name']]['voltage'] = 'High alarm'
            exitcode = 2
        elif float(interface['optics-diagnostics']['module-voltage-low-warn-threshold']) >= float(interface['optics-diagnostics']['module-voltage']):
            result[interface['name']]['voltage'] = 'Low warn'
            if exitcode != 2:
                exitcode = 1
        elif float(interface['optics-diagnostics']['module-voltage-high-warn-threshold']) <= float(interface['optics-diagnostics']['module-voltage']):
            result[interface['name']]['voltage'] = 'High Warn'
            if exitcode != 2:
                exitcode = 1
        else:
            result[interface['name']]['voltage'] = 'OK'

        if float(interface['optics-diagnostics']['laser-rx-power-low-alarm-threshold-dbm']) >= float(interface['optics-diagnostics']['rx-signal-avg-optical-power-dbm']):
            result[interface['name']]['rx-power'] = 'Low alarm'
            exitcode = 2
        elif float(interface['optics-diagnostics']['rx-signal-avg-optical-power-dbm']) >= float(interface['optics-diagnostics']['laser-rx-power-high-alarm-threshold-dbm']):
            result[interface['name']]['rx-power'] = 'High alarm'
            exitcode = 2
        elif float(interface['optics-diagnostics']['laser-rx-power-low-warn-threshold-dbm']) >= float(interface['optics-diagnostics']['rx-signal-avg-optical-power-dbm']):
            result[interface['name']]['rx-power'] = 'Low warn'
            if exitcode != 2:
                exitcode = 1
        elif float(interface['optics-diagnostics']['laser-rx-power-high-warn-threshold-dbm']) <= float(interface['optics-diagnostics']['rx-signal-avg-optical-power-dbm']):
            result[interface['name']]['rx-power'] = 'High alarm'
            if exitcode != 2:
                exitcode = 1
        else:
            result[interface['name']]['rx-power'] = 'OK'
pprint(result)
dev.close()
exit(exitcode)
