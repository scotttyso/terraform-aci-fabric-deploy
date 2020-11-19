#!/usr/bin/env python3

import validators
import re
import ipaddress


# Validations
def validate_bgp_as(line_count, bgp_as):
    bgp_as=int(bgp_as)
    if not validators.between(bgp_as, min=1, max=4294967295):
        print(f"----------------\r")
        print(f"  Error on Row {line_count}. BGP AS {bgp_as} is invalid.")
        print(f"  A valid BGP AS is between 1 and 4294967295.  Exiting....")
        print("----------------")
        exit()


def validate_hostname(line_count, name):
    pattern = re.compile('^[a-zA-Z0-9\\-]+$')
    if not re.search(pattern, name) and validators.length(name, min=1, max=63):
        print(f"----------------\r")
        print(f"  Error on Row {line_count}. {name} is not a valid Hostname.")
        print(f"  Be sure you are not using the FQDN.  Exiting....")
        print("----------------")
        exit()


def validate_inb_vlan(line_count, inb_vlan):
    inb_vlan=int(inb_vlan)
    if not validators.between(inb_vlan, min=2, max=4094):
        print(f"----------------\r")
        print(f"  Error on Row {line_count}. Inband Vlan {inb_vlan} is invalid.")
        print(f"  A valid Inband Vlan is between 2 and 4094.  Exiting....")
        print("----------------")
        exit()


def validate_node_id(line_count, name, node_id):
    node_id=int(node_id)
    if not validators.between(node_id, min=101, max=4001):
        print(f"----------------\r")
        print(f"  Error on Row {line_count}. {name} node_id {node_id} is invalid.")
        print(f"  A valid Node ID is between 101 and 4000.  Exiting....")
        print("----------------")
        exit()


def validate_node_id_apic(line_count, name, node_id):
    node_id=int(node_id)
    if not validators.between(node_id, min=1, max=7):
        print(f"----------------\r")
        print(f"  Error on Row {line_count}. APIC node_id {node_id} is invalid.")
        print(f"  A valid Node ID is between 1 and 7.  Exiting....")
        print("----------------")
        exit()


def validate_node_type(line_count, name, node_type):
    pattern = re.compile('^(remote-leaf-wan|unspecified)$')
    if not re.search(pattern, node_type):
        print(f"----------------\r")
        print(f"  Error on Row {line_count}. {name} node_type {node_type} is not valid.")
        print(f"  Valid node_types are remote-leaf-wan or unspecified.  Exiting....")
        print("----------------")
        exit()


def validate_pod_id(line_count, name, pod_id):
    pod_id=int(pod_id)
    if not validators.between(pod_id, min=1, max=12):
        print(f"----------------\r")
        print(f"  Error on Row {line_count}. {name} pod_id {pod_id} is invalid.")
        print(f"  A valid Pod ID is between 1 and 12.  Exiting....")
        print("----------------")
        exit()


def validate_role(line_count, name, switch_role):
    pattern = re.compile('^(leaf|spine)$')
    if not re.search(pattern, switch_role):
        print(f"----------------\r")
        print(f"  Error on Row {line_count}. {name} role {switch_role} is not valid.")
        print(f"  Valid switch_roles are leaf or spine, which are required by the")
        print(f"  script to determine resources to build.  Exiting....")
        print("----------------")
        exit()


def validate_modules(line_count, name, switch_role, modules):
    modules = int(modules)
    module_count = 0
    if switch_role == 'leaf' and modules == 1:
        module_count += 1
    elif switch_role == 'leaf':
        print(f"----------------\r")
        print(f"  Error on Row {line_count}. {name} module count is not valid.")
        print(f"  A Leaf can only have one module.  Exiting....")
        print("----------------")
        exit()
    elif switch_role == 'spine' and modules < 17:
        module_count += 1
    elif switch_role == 'spine':
        print(f"----------------\r")
        print(f"  Error on Row {line_count}. {name} module count is not valid.")
        print(f"  A Spine needs between 1 and 16 modules.  Exiting....")
        print("----------------")
        exit()


def validate_port_count(line_count, name, switch_role, port_count):
    pattern = re.compile('^(32|36|48|64|96)$')
    if not re.search(pattern, port_count):
        print(f"----------------\r")
        print(f"  Error on Row {line_count}. {name} port count of {port_count} is not valid.")
        print(f"  Valid port counts are 32, 36, 48, 64, 96.  Exiting....")
        print("----------------")
        exit()


def validate_inband(line_count, name, inb_ipv4, inb_gwv4):
    inb_check_ipv4 = ipaddress.IPv4Interface(inb_ipv4)
    inb_network_v4 = inb_check_ipv4.network
    if not ipaddress.IPv4Address(inb_gwv4) in ipaddress.IPv4Network(inb_network_v4):
        print(f"\r\r----------------\r")
        print(f"  Error on Row {line_count}. {name} InBand Network doesn't Match Gateway Network.")
        print(f"  IPv4 Address {inb_ipv4}")
        print(f"  IPv4 Gateway {inb_gwv4}")
        print(f"  Exiting...")
        print('----------------\r\r')
        exit()


def validate_ipv4(line_count, ipv4):
    if not ipaddress.IPv4Address(ipv4):
        print(f"----------------")
        print(f"  Error on Row {line_count}. {ipv4} is not a valid IPv4 Address.")
        print(f"  Exiting...")
        print("----------------")
        exit()


def validate_mgmt_domain(line_count, mgmt_domain):
    if mgmt_domain == 'oob':
        mgmt_domain = 'oob-default'
    elif mgmt_domain == 'inband':
        mgmt_domain = 'inb-inb_epg'
    else:
        print('\r----------------\r')
        print(f'   Error, the Management Domain Should be inband or oob')
        print(f'   Error on Row {line_count}, Please verify input information.')
        print('----------------\r')
        exit()
    return mgmt_domain


def validate_oob(line_count, name, oob_ipv4, oob_gwv4):
    oob_check_ipv4 = ipaddress.IPv4Interface(oob_ipv4)
    oob_network_v4 = oob_check_ipv4.network
    if not ipaddress.IPv4Address(oob_gwv4) in ipaddress.IPv4Network(oob_network_v4):
        print(f"----------------")
        print(f"  Error on Row {line_count}. {name} Out-of-Band Network doesn't Match Gateway Network.")
        print(f"  IPv4 Address {oob_ipv4}")
        print(f"  IPv4 Gateway {oob_gwv4}")
        print(f"  Exiting...")
        print("----------------")
        exit()


def validate_snmp_mgmt(line_count, mgmt_domain):
    if mgmt_domain == 'oob':
        mgmt_domain = 'Out-of-Band'
    elif mgmt_domain == 'inband':
        mgmt_domain = 'Inband'
    else:
        print('\r----------------\r')
        print(f'   Error, the Management Domain Should be inband or oob')
        print(f'   Error on Row {line_count}, Please verify input information.')
        print('----------------\r')
        exit()
    return mgmt_domain


