import csv
import ipaddress
import re, sys, traceback, validators

if len(sys.argv) > 2:
    csv_input = sys.argv[1]
    append = sys.argv[1]
else:
    csv_input = sys.argv[1]
    append = 'no'

file_dns = 'resources_dns.tf'
file_sw = 'resources_switches.tf'
file_time = 'resources_time.tf'
file_tenants = 'resources_default_tenants.tf'

if append == 'yes':
    wr_file_dns = open(file_dns, 'a')
else:
    wr_file_dns = open(file_dns, 'w')

if append == 'yes':
    wr_file_sw = open(file_sw, 'a')
else:
    wr_file_sw = open(file_sw, 'w')

if append == 'yes':
    wr_file_time = open(file_time, 'a')
else:
    wr_file_time = open(file_time, 'w')

if append == 'yes':
    wr_file_tenants = open(file_tenants, 'a')
else:
    wr_file_tenants = open(file_tenants, 'w')

def validate_hostname(line_count, name):
    pattern = re.compile('^[a-zA-Z0-9\-]+$')
    if not re.search(pattern, name) and validators.length(name, min=1, max=63):
        print(f"----------------\r")
        print(f"  Error on Row {line_count}. {name} is not a valid Hostname.")
        print(f"  Be sure you are not using the FQDN.  Exiting....")
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
    pattern = re.compile('^(leaf|spine|unspecified)$')
    if not re.search(pattern, switch_role):
        print(f"----------------\r")
        print(f"  Error on Row {line_count}. {name} role {switch_role} is not valid.")
        print(f"  Valid switch_roles are leaf or spine or unspecified.  Exiting....")
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

def resource_switch(serial, name, node_id, node_type, pod_id, switch_role, inb_ipv4, inb_gwv4, oob_ipv4, oob_gwv4):
    try:
        # Validate Serial Number
        
        # Validate Hostname
        validate_hostname(line_count, name)
        
        # Validate Node_ID
        validate_node_id(line_count, name, node_id)

        # Validate node_type
        validate_node_type(line_count, name, node_type)

        # Validate Pod_ID
        validate_pod_id(line_count, name, pod_id)

        # Validate switch role
        validate_role(line_count, name, switch_role)

        # Validate InBand Network
        validate_inband(line_count, name, inb_ipv4, inb_gwv4)

        # Validate Out-of-Band Network

    except Exception as err:
        print('\r\r----------------\r')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}, Please verify input information.')
        print('----------------\r\r')
        exit()
    wr_file_sw.write('\n')
    wr_file_sw.write('resource "aci_fabric_node_member" "%s" {\n' % name)
    wr_file_sw.write('\tserial = "%s"\n' % serial)
    wr_file_sw.write('\tname = "%s"\n' % name)
    wr_file_sw.write('\tnode_id = "%s"\n' % node_id)
    wr_file_sw.write('\tnode_type = "%s"\n' % node_type)
    wr_file_sw.write('\trole = "%s"\n' % switch_role)
    wr_file_sw.write('\tpod_id = "%s"\n' % pod_id)
    wr_file_sw.write('}\n')


try:
    open(csv_input)
except IOError:
    print(f"----------------")
    print(f"  {csv_input} does not exist")
    print(f"  Exiting...")
    print(f"----------------")
    exit()

with open(csv_input) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for column in csv_reader:
        if any(column):        
            type = column[0]
            if type == 'Company':
                line_count += 1
            elif type == 'dns':
                line_count += 1
            elif type == 'switch':
                    serial = column[1]
                    name = column[2]
                    node_id = column[3]
                    node_type = column[4]
                    pod_id = column[5]
                    switch_role = column[6]
                    inb_ipv4 = column[7]
                    inb_gwv4 = column[8]
                    oob_ipv4 = column[9]
                    oob_gwv4 = column[10]
                    
                    # Create Resource Record for Switch
                    resource_switch(serial, name, node_id, node_type, pod_id, switch_role, inb_ipv4, inb_gwv4, oob_ipv4, oob_gwv4)
                    
                    # Increment Line Count
                    line_count += 1
            elif type == 'time':
                line_count += 1
            elif type == 'tenants':
                line_count += 1
            else:
                line_count += 1
        else:
            line_count += 1

#Close out the Open Files
csv_file.close()
wr_file_dns.close()
wr_file_sw.close()
wr_file_time.close()
wr_file_tenants.close()

#End Script
print('\r\r----------------\r')
print(f'  Completed Running Script')
print(f'  Exiting...')
print('----------------\r\r')
exit()