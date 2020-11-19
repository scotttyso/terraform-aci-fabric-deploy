import csv
#import ipaddress
import re, sys, traceback, validators
#import json
#import os
#import testvalidator
import terraformresources


template_m = '{0} {1}\n\tpath\t\t= {2}\n\tclass_name\t= {3}\n\tpayload\t\t= <<EOF\n{4}\n\tEOF\n{5}\n\n'
append = ""
cvs_input = ""


if len(sys.argv) == 2:
    csv_input = sys.argv[1]
    append = sys.argv[1]
elif len(sys.argv) == 1:
    csv_input = sys.argv[1]
    append = 'no'

try:
    with open(csv_input, 'r') as truth:
        pass
except IOError:
    print(f"----------------")
    print(f"  {csv_input} does not exist")
    print(f"  Exiting...")
    print(f"----------------")
    exit()

file_base_pod_info = 'resources_user_import_Fabric_Policies.tf'

if append == 'yes':
    wr_base_info = open(file_base_pod_info, 'a')
else:
    wr_base_info = open(file_base_pod_info, 'w')
    wr_base_info.write('# This File will include DNS, Domain, NTP, Timezone and other base configuration parameters\n')


with open(csv_input) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    count_inb_gwv4 = 0
    count_inb_vlan = 0
    count_dns_servers = 0
    inb_vlan = ''
    for column in csv_reader:
        if any(column):
            type = column[0]
            if type == 'apic_inb':
                name = column[1]
                node_id = column[2]
                pod_id = column[3]
                inb_ipv4 = column[4]
                inb_gwv4 = column[5]
                p1_leaf = column[6]
                p1_swpt = column[7]
                p2_leaf = column[8]
                p2_swpt = column[9]

                # Make sure the inband_vlan exists
                if not inb_vlan:
                    print(f"----------------")
                    print(f"  The Inband VLAN must be defined before configuring management")
                    print(f"  on all switches.  Please first add the Inband VLAN to the")
                    print(f"  definitions.  Exiting...")
                    print(f"----------------")
                    exit()

                # Create Resource Record for Switch and inband Bridge  Domain AP/EPG
                terraformresources.resource_apic_inb(name, node_id, pod_id, inb_ipv4, inb_gwv4, inb_vlan, p1_leaf, p1_swpt, p2_leaf, p2_swpt, line_count)
                if count_inb_gwv4 == 0:
                    terraformresources.resource_inband(inb_ipv4, inb_gwv4, inb_vlan, line_count)
                    count_inb_gwv4 += 1
                    current_inb_gwv4 = inb_gwv4
                else:
                    if not current_inb_gwv4 == inb_gwv4:
                            print(f"----------------")
                            print(f"  current inband = {current_inb_gwv4} and found {inb_gwv4} next")
                            print(f"  The Inband Network should be the same on all APIC's and Switches.")
                            print(f"  Different Gateway's were found")
                            print(f"  Exiting...")
                            print(f"----------------")
                            exit()
                line_count += 1
            elif type == 'bgp_as':
                bgp_as = column[1]
                # Configure the Default BGP AS Number
                terraformresources.resource_bgp_as(bgp_as, line_count, wr_base_info)
                line_count += 1
            elif type == 'bgp_rr':
                node_id = column[2]
                # Configure the Default BGP Route Reflector
                terraformresources.resource_bgp_rr(node_id, line_count, bgp_as, wr_base_info)
                line_count += 1
            elif type == 'Company':
                line_count += 1
            elif type == 'dns':
                dns_ipv4 = column[1]
                prefer = column[2]
                if count_dns_servers < 2:
                    # Create Resource Record for DNS Servers
                    terraformresources.resource_dns(dns_ipv4, prefer, line_count, wr_base_info)
                else:
                    print(f"----------------")
                    print(f"  At this time it is only supported to add two DNS Providers")
                    print(f"  Remove one or more providers.  Exiting....")
                    print(f"----------------")
                    exit()
                count_dns_servers += 1
                line_count += 1
            elif type == 'dns_mgmt':
                mgmt_domain = column[1]
                # Create Resource Record for DNS Servers
                terraformresources.resource_dns_mgmt(mgmt_domain, line_count, wr_base_info)
                line_count += 1
            elif type == 'search_domain':
                domain = column[1]
                prefer = column[2]
                # Create Resource Record for Search Domain
                terraformresources.resource_domain(domain, prefer, wr_base_info)
                line_count += 1
            elif type == 'inband_vlan':
                inb_vlan = column[1]
                line_count += 1
            elif type == 'ntp':
                ntp_ipv4 = column[1]
                prefer = column[2]
                mgmt_domain = column[3]
                # Create Resource Record for NTP Servers
                terraformresources.resource_ntp(ntp_ipv4, prefer, mgmt_domain, line_count, wr_base_info)
                line_count += 1
            elif type == 'snmp_client':
                client_name = column[1]
                client_ipv4 = column[2]
                mgmt_domain = column[3]
                # Create Resource Record for SNMP Client
                terraformresources.resource_snmp_client(client_name, client_ipv4, mgmt_domain, line_count, wr_base_info)
                line_count += 1
            elif type == 'snmp_comm':
                community = column[1]
                description = column[2]
                # Create Resource Record for SNMP Communities
                terraformresources.resource_snmp_comm(community, description, wr_base_info)
                line_count += 1
            elif type == 'snmp_info':
                contact = column[1]
                location = column[2]
                # Create Resource Record for SNMP Default Policy
                terraformresources.resource_snmp_info(contact, location, wr_base_info)
                line_count += 1
            elif type == 'snmp_trap':
                snmp_ipv4 = column[1]
                snmp_port = column[2]
                # Create Resource Record for SNMP Traps
                terraformresources.resource_snmp_trap(snmp_ipv4, snmp_port, line_count, wr_base_info)
                line_count += 1
            elif type == 'snmp_user':
                snmp_user = column[1]
                priv_type = column[2]
                priv_key = column[3]
                auth_type = column[4]
                auth_key = column[5]
                # Create Resource Record for SNMP Users
                terraformresources.resource_snmp_user(snmp_user, priv_type, priv_key, auth_type, auth_key, line_count, wr_base_info)
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
                oob_ipv4 = column[9]
                oob_gwv4 = column[10]
                inb_ipv4 = column[11]
                inb_gwv4 = column[12]

                # Make sure the inband_vlan exists
                if not inb_vlan:
                    print(f"----------------")
                    print(f"  The Inband VLAN must be defined before configuring management")
                    print(f"  on all switches.  Please first add the Inband VLAN to the")
                    print(f"  definitions.  Exiting...")
                    print(f"----------------")
                    exit()

                # Create Resource Record for Switch and inband Bridge  Domain AP/EPG
                terraformresources.resource_switch(serial, name, node_id, node_type, pod_id, switch_role, modules, port_count, oob_ipv4, oob_gwv4,
                                inb_ipv4, inb_gwv4, inb_vlan, line_count)
                if count_inb_gwv4 == 0:
                    terraformresources.resource_inband(inb_ipv4, inb_gwv4, inb_vlan, line_count)
                    count_inb_gwv4 += 1
                    current_inb_gwv4 = inb_gwv4
                else:
                    if not current_inb_gwv4 == inb_gwv4:
                            print(f"----------------")
                            print(f"  current inband = {current_inb_gwv4} and found {inb_gwv4} next")
                            print(f"  The Inband Network should be the same on all APIC's and Switches.")
                            print(f"  Different Gateway's were found")
                            print(f"  Exiting...")
                            print(f"----------------")
                            exit()

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


# Close out the Open Files
csv_file.close()
wr_base_info.close()


# End Script
print('\r\r----------------\r')
print(f'  Completed Running Script')
print(f'  Exiting...')
print('----------------\r\r')
exit()
