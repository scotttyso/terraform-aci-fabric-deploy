import csv
import ipaddress
import re, sys, traceback, validators

if len(sys.argv) == 2:
    csv_input = sys.argv[1]
    append = sys.argv[1]
elif len(sys.argv) == 1:
    csv_input = sys.argv[1]
    append = 'no'

file_basic_pod_info = 'resources_user_import_base_pod_policies.tf'

if append == 'yes':
    wr_file_basic_pod_info = open(file_basic_pod_info, 'a')
else:
    wr_file_basic_pod_info = open(file_basic_pod_info, 'w')

def validate_hostname(line_count, name):
    pattern = re.compile('^[a-zA-Z0-9\\-]+$')
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

def resource_switch(serial, name, node_id, node_type, pod_id, switch_role, modules, port_count, inb_ipv4, inb_gwv4, oob_ipv4, oob_gwv4):
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

        # Validate Modules
        validate_modules(line_count, name, switch_role, modules)

        # Validate port_count
        validate_port_count(line_count, name, switch_role, port_count)

        # Validate InBand Network
        validate_inband(line_count, name, inb_ipv4, inb_gwv4)

        # Validate Out-of-Band Network
        validate_oob(line_count, name, oob_ipv4, oob_gwv4)

    except Exception as err:
        print('\r\r----------------\r')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}, Please verify input information.')
        print('----------------\r\r')
        exit()
    pod_id = str(pod_id)
    file_sw = ('resources_user_import_%s.tf' % (name))
    wr_file_sw = open(file_sw, 'w')
    wr_file_sw.write(f'# Use this Resource File to Register {name} with node id {node_id} to the Fabric\n')
    wr_file_sw.write('# Requirements are:\n')
    wr_file_sw.write('# serial: Actual Serial Number of the switch.\n')
    wr_file_sw.write('# name: Hostname you want to assign.\n')
    wr_file_sw.write('# node_id: unique ID used to identify the switch in the APIC.\n')
    wr_file_sw.write('#   in the "Cisco ACI Object Naming and Numbering: Best Practice\n')
    wr_file_sw.write('#   The recommendation is that the Spines should be 101-199\n')
    wr_file_sw.write('#   and leafs should start at 200+ thru 4000.  As the number of\n')
    wr_file_sw.write('#   spines should always be less than the number of leafs\n')
    wr_file_sw.write('#   https://www.cisco.com/c/en/us/td/docs/switches/datacenter/aci/apic/sw/kb/b-Cisco-ACI-Naming-and-Numbering.html#id_107280\n')
    wr_file_sw.write('# node_type: uremote-leaf-wan or unspecified.\n')
    wr_file_sw.write('# role: spine, leaf, or unspecified.\n')
    wr_file_sw.write('# pod_id: Typically this will be one unless you are running multipod.\n')
    dummy_number = 0
    wr_file_sw.write('\n')
    wr_file_sw.write('resource "aci_fabric_node_member" "%s" {\n' % (name))
    wr_file_sw.write('\tserial    = "%s"\n' % (serial))
    wr_file_sw.write('\tname      = "%s"\n' % (name))
    wr_file_sw.write('\tnode_id   = "%s"\n' % (node_id))
    wr_file_sw.write('\tnode_type = "%s"\n' % (node_type))
    wr_file_sw.write('\trole      = "%s"\n' % (switch_role))
    wr_file_sw.write('\tpod_id    = "%s"\n' % (pod_id))
    wr_file_sw.write('}\n')
    wr_file_sw.write('\n')
    wr_file_sw.write('resource "aci_rest" "oob_mgmt_%s" {\n' % (name))
    wr_file_sw.write('\tpath       = "/api/node/mo/uni/tn-mgmt"\n')
    wr_file_sw.write('\tclass_name = "mgmtRsOoBStNode"\n')
    wr_file_sw.write('\tpayload    = <<EOF\n')
    wr_file_sw.write('{\n')
    wr_file_sw.write('\t"mgmtRsOoBStNode": {\n')
    wr_file_sw.write('\t\t"attributes": {\n')
    wr_file_sw.write('\t\t\t"addr":"%s",\n' % (oob_ipv4))
    wr_file_sw.write('\t\t\t"dn":"uni/tn-mgmt/mgmtp-default/oob-default/rsooBStNode-[topology/pod-%s/node-%s]",\n' % (pod_id, node_id))
    wr_file_sw.write('\t\t\t"gw":"%s",\n' % (oob_gwv4))
    wr_file_sw.write('\t\t\t"tDn":"topology/pod-%s/node-%s",\n' % (pod_id, node_id))
    wr_file_sw.write('\t\t\t"v6Addr":"::",\n')
    wr_file_sw.write('\t\t\t"v6Gw":"::"\n')
    wr_file_sw.write('\t\t}\n')
    wr_file_sw.write('\t}\n')
    wr_file_sw.write('}\n')
    wr_file_sw.write('\tEOF\n')
    wr_file_sw.write('}\n')
    wr_file_sw.write('\n')
    wr_file_sw.write('resource "aci_rest" "inband_mgmt_%s" {\n' % (name))
    wr_file_sw.write('\tpath       = "/api/node/mo/uni/tn-mgmt"\n')
    wr_file_sw.write('\tclass_name = "mgmtRsInBStNode"\n')
    wr_file_sw.write('\tpayload    = <<EOF\n')
    wr_file_sw.write('{\n')
    wr_file_sw.write('\t"mgmtRsInBStNode": {\n')
    wr_file_sw.write('\t\t"attributes": {\n')
    wr_file_sw.write('\t\t\t"addr":"%s",\n' % (inb_ipv4))
    wr_file_sw.write('\t\t\t"dn":"uni/tn-mgmt/mgmtp-default/inb-inband_epg/rsinBStNode-[topology/pod-%s/node-%s]",\n' % (pod_id, node_id))
    wr_file_sw.write('\t\t\t"gw":"%s",\n' % (inb_gwv4))
    wr_file_sw.write('\t\t\t"tDn":"topology/pod-%s/node-%s",\n' % (pod_id, node_id))
    wr_file_sw.write('\t\t}\n')
    wr_file_sw.write('\t}\n')
    wr_file_sw.write('}\n')
    wr_file_sw.write('\tEOF\n')
    wr_file_sw.write('}\n')
    wr_file_sw.write('\n')

    if switch_role == 'leaf':
        wr_file_sw.write('resource "aci_leaf_profile" "%s" {\n' % (name))
        wr_file_sw.write('\tname = "%s"\n' % (name))
        wr_file_sw.write('\tleaf_selector {\n')
        wr_file_sw.write('\t\tname                    = "%s"\n' % (name))
        wr_file_sw.write('\t\tswitch_association_type = "range"\n')
        wr_file_sw.write('\t\tnode_block {\n')
        wr_file_sw.write('\t\t\tname  = "%s"\n' % (name))
        wr_file_sw.write('\t\t\tfrom_ = "%s"\n' % (node_id))
        wr_file_sw.write('\t\t\tto_   = "%s"\n' % (node_id))
        wr_file_sw.write('\t\t}\n')
        wr_file_sw.write('\t}\n')
        wr_file_sw.write('}\n')
        wr_file_sw.write('\n')
        wr_file_sw.write('resource "aci_leaf_interface_profile" "%s" {\n' % (name))
        wr_file_sw.write('\tname = "%s"\n' % (name))
        wr_file_sw.write('}\n')
        wr_file_sw.write('\n')
        wr_file_sw.write('resource "aci_rest" "leaf_int_selector_%s" {\n' % (name))
        wr_file_sw.write('\tpath       = "/api/node/mo/uni/infra/nprof-%s.json"\n' % (name))
        wr_file_sw.write('\tclass_name = "infraRsAccPortP"\n')
        wr_file_sw.write('\tpayload    = <<EOF\n')
        wr_file_sw.write('{\n')
        wr_file_sw.write('\t"infraRsAccPortP": {\n')
        wr_file_sw.write('\t\t"attributes": {\n')
        wr_file_sw.write('\t\t\t"tDn": "uni/infra/accportprof-%s"\n' % (name))
        wr_file_sw.write('\t\t}\n')
        wr_file_sw.write('\t}\n')
        wr_file_sw.write('}\n')
        wr_file_sw.write('\tEOF\n')
        wr_file_sw.write('}\n')
        wr_file_sw.write('\n')
        mod_count = 0
        while mod_count < int(modules):
            mod_count += 1
            wr_file_sw.write('resource "aci_access_port_selector" "%s" {\n' % (name))
            wr_file_sw.write('\tfor_each                  = var.port_selector_%s\n' %(port_count))
            wr_file_sw.write('\tleaf_interface_profile_dn = aci_leaf_interface_profile.%s.id\n' % (name))
            wr_file_sw.write('\tname                      = Eth%s-[each.value.name]\n' % (mod_count))
            wr_file_sw.write('\taccess_port_selector_type = "range"\n')
            wr_file_sw.write('}\n')
            wr_file_sw.write('\n')
    elif switch_role == 'spine':
        dummy_number += 1
    wr_file_sw.close()



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
                    modules = column[7]
                    port_count = column[8]
                    inb_ipv4 = column[9]
                    inb_gwv4 = column[10]
                    oob_ipv4 = column[11]
                    oob_gwv4 = column[12]
                    
                    # Create Resource Record for Switch
                    resource_switch(serial, name, node_id, node_type, pod_id, switch_role, modules, port_count, inb_ipv4, inb_gwv4, 
                                    oob_ipv4, oob_gwv4)
                    
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
wr_file_basic_pod_info.close()

#End Script
print('\r\r----------------\r')
print(f'  Completed Running Script')
print(f'  Exiting...')
print('----------------\r\r')
exit()