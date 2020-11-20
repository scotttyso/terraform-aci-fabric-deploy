#!/usr/bin/env python3

import csv
import ipaddress
import json
import phonenumbers
import os, re, sys, traceback, validators
import validating
from datetime import datetime, timedelta

if len(sys.argv) == 2:
    csv_input = sys.argv[1]
    append = sys.argv[1]
elif len(sys.argv) == 1:
    csv_input = sys.argv[1]
    append = 'no'

try:
    open(csv_input)
except IOError:
    print(f"----------------")
    print(f"  {csv_input} does not exist")
    print(f"  Exiting...")
    print(f"----------------")
    exit()

# Creating User Input Fabric Policies File to attached policies for
# DNS, Domain, NTP, SmartCallHome, SNMP, Syslog, TACACS Accounting etc.
file_base_pod_info = 'resources_user_import_Fabric_Policies.tf'
if append == 'yes':
    wr_base_info = open(file_base_pod_info, 'a')
else:
    wr_base_info = open(file_base_pod_info, 'w')
    wr_base_info.write('# This File will include DNS, Domain, NTP, SmartCallHome\n# SNMP, Syslog and other base configuration parameters\n')

# SNMP requires assigning Communities to Tenant VRF's.
# These files are used to capture Communities Defined
# At the Fabric Level to then Assign to the Mgmt Tenant VRF's
file_comm = 'snmp_comms.txt'
wr_comm = open(file_comm, 'a')
file_vrfs = 'vrfs.txt'
wr_vrfs = open(file_vrfs, 'a')

def template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file):
    template_payload = '{0} {1}\n\tpath\t\t= {2}\n\tclass_name\t= "{3}"\n\tpayload\t\t= <<EOF\n{4}\n\tEOF\n{5}\n\n'

    resource_line = 'resource "aci_rest" "{}"'.format(resrc_desc)

    # Attached Data to template
    wr_to_file = template_payload.format(resource_line, "{", path_attrs, class_name, json.dumps(data_out, indent=4), "}")

    # Write Data to Template
    wr_file.write(wr_to_file)

def template_aci_terraform(resrc_type, resrc_desc, attr_1st, attr_2nd, attr_3rd, wr_file):
    template_payload = '{0} {1}\n\t{2}\n\t{3}\n\t{4}\n{5}\n\n'

    resource_line = 'resource "{}" "{}"'.format(resrc_type, resrc_desc)

    wr_to_file = template_payload.format(resource_line, "{", attr_1st, attr_2nd, attr_3rd, "}")
    # Write Data to Template
    wr_file.write(wr_to_file)

def resource_apic_inb(name, node_id, pod_id, inb_ipv4, inb_gwv4, inb_vlan, p1_leaf, p1_swpt, p2_leaf, p2_swpt):
    try:
        # Validate APIC Node_ID
        validating.node_id_apic(line_count, name, node_id)

        # Validate Pod_ID
        validating.pod_id(line_count, name, pod_id)

        # Validate InBand Network
        validating.inband(line_count, name, inb_ipv4, inb_gwv4)
    except Exception as err:
        print('\r\r----------------\r')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}, Please verify input information.')
        print('----------------\r\r')
        exit()
    
    # Convert pod_id from integer to String
    pod_id = str(pod_id)

    # Which File to Write Data to
    apic_file = 'resources_user_import_xDevice_{}.tf'.format(name)
    wr_file = open(apic_file, 'w')

    # Define Variables for Template Creation
    resrc_desc = 'inb_mgmt_apic_{}'.format(name)
    class_name = 'mgmtRsInBStNode'
    tDn_string = "topology/pod-{}/node-{}".format(pod_id, node_id)
    dn_strings = "uni/tn-mgmt/mgmtp-default/inb-inb_epg/rsinBStNode-[topology/pod-{}/node-{}]".format(pod_id, node_id)
    path_attrs = '"/api/node/mo/uni/tn-mgmt.json"'

    base_atts = {'dn': dn_strings, 'addr': inb_ipv4, 'gw': inb_gwv4, 'tDn': tDn_string}
    data_out = {class_name: {'attributes': base_atts, 'children': []}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

    # Combine Input Port Information to read as List
    list_ports = [p1_leaf + ',' + p1_swpt,p2_leaf + ',' + p2_swpt]
    port_list_count = 0
    for x in list_ports:
        port_list_count += 1
        var_list = x.split(',')
        leaf = var_list[0]
        port_x = var_list[1]
        port_split = port_x.split('/')
        module = port_split[0]
        port = port_split[1]

        # Define Variables for Template Creation
        resrc_desc = '{}_port_2_{}'.format(name, port_list_count)
        class_name = 'infraRsAccBaseGrp'
        tDn_string = "uni/infra/funcprof/accportgrp-inband_ap"
        path_attrs = '"/api/node/mo/uni/infra/accportprof-{}_IntProf/hports-Eth{}-{}-typ-range/rsaccBaseGrp.json"'.format(leaf, module, port)

        base_atts = {'tDn': tDn_string}
        data_out = {class_name: {'attributes': base_atts, 'children': []}}

        # Write Output to Resource Files using Template
        template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

    # Close the File created for this resource
    wr_file.close()

def resource_bgp_as(bgp_as):
    # Validate BGP AS Number
    validating.bgp_as(line_count, bgp_as)
        
    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation
    resrc_desc = 'bgp_as_{}'.format(bgp_as)
    class_name = "bgpAsP"
    rn_strings = "as"
    dn_strings = "uni/fabric/bgpInstP-default/{}".format(rn_strings)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)

    base_atts = {'dn': dn_strings, 'asn': bgp_as, 'rn': rn_strings}
    data_out = {class_name: {'attributes': base_atts, 'children': []}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)
    
def resource_bgp_rr(node_id):
    # Validate Node ID
    validating.node_id(line_count, node_id)
        
    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation
    resrc_desc = 'bgp_rr_{}'.format(node_id)
    class_name = 'bgpRRNodePEp'
    rn_strings = "node-{}".format(node_id)
    dn_strings = "uni/fabric/bgpInstP-default/rr/node-{}".format(node_id)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)

    base_atts = {'dn': dn_strings, 'id': node_id, 'rn': rn_strings}
    data_out = {class_name: {'attributes': base_atts, 'children': []}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

def resource_dns(dns_ipv4, prefer):
    # Validate DNS IPv4 Address
    try:
        validating.ipv4(line_count, dns_ipv4)
    except Exception as err:
        print('\r\r----------------\r')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}, Please verify input information.')
        print('----------------\r\r')
        exit()
    
    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation
    dns_ipv4_ = dns_ipv4.replace('.', '_')
    resrc_desc = 'dns_{}'.format(dns_ipv4_)
    class_name = 'dnsProv'
    rn_strings = "prov-[{}]".format(dns_ipv4)
    dn_strings = "uni/fabric/dnsp-default/{}".format(rn_strings)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)

    base_atts = {'dn': dn_strings, 'addr': dns_ipv4, 'preferred': prefer, 'rn': rn_strings}
    data_out = {class_name: {'attributes': base_atts, 'children': []}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

def resource_dns_mgmt(mgmt_domain):
    # Validate Management Domain
    mgmt_epg = validating.mgmt_domain(line_count, mgmt_domain)
        
    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation
    resrc_desc = 'dns_epg_{}'.format(mgmt_epg)
    class_name = 'dnsRsProfileToEpg'
    tDn_string = "uni/tn-mgmt/mgmtp-default/{}".format(mgmt_epg)
    path_attrs = '"/api/node/mo/uni/fabric/dnsp-default.json"'

    base_atts = {'tDn': tDn_string}
    data_out = {class_name: {'attributes': base_atts, 'children': []}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

def resource_domain(domain, prefer):

    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation
    domain_ = domain.replace('.', '_')
    resrc_desc = 'domain_{}'.format(domain_)
    class_name = 'dnsDomain'
    rn_strings = "dom-[{}]".format(domain)
    dn_strings = "uni/fabric/dnsp-default/{}".format(rn_strings)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)

    base_atts = {'dn': dn_strings, 'name': domain, 'isDefault': prefer, 'rn': rn_strings}
    data_out = {class_name: {'attributes': base_atts, 'children': []}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

def resource_inband(inb_ipv4, inb_gwv4, inb_vlan):
    
    # Validate Inband VLAN
    try:
        validating.inb_vlan(line_count, inb_vlan)
    except Exception as err:
        print('\r\r----------------\r')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}, Please verify input information.')
        print('----------------\r\r')
        exit()

    # Which File to Write Data to
    file_inb = ('resources_user_import_Tenant_Mgmt.tf')
    wr_file = open(file_inb, 'w')
    wr_file.write('# Use this Resource File to Register the inband management network for the Fabric\n\n')

    
    # Define Variables for Template Creation
    gwy_prefix = inb_ipv4.split('/', 2)
    gateway_v4 = str(inb_gwv4) + '/' + str(gwy_prefix[1])

    # Resource for Inband Subnet
    resrc_type = 'aci_subnet'
    resrc_desc = 'inb_subnet'
    attr_1st = 'parent_dn\t= aci_bridge_domain.inb.id'
    attr_2nd = 'ip\t\t\t= "{}"'.format(gateway_v4)
    attr_3rd = 'scope\t\t= ["public"]'

    # Write Output to Resource Files using Template
    template_aci_terraform(resrc_type, resrc_desc, attr_1st, attr_2nd, attr_3rd, wr_file)

    # Resource for Inband VLAN
    resrc_type = 'aci_ranges'
    resrc_desc = 'inb_vlan'
    attr_1st = 'vlan_pool_dn	= "uni/infra/vlanns-[inband_vl-pool]-static"'
    attr_2nd = '_from		    = "vlan-{}"'.format(inb_vlan)
    attr_3rd = 'to		        = "vlan-{}"'.format(inb_vlan)

    # Write Output to Resource Files using Template
    template_aci_terraform(resrc_type, resrc_desc, attr_1st, attr_2nd, attr_3rd, wr_file)

    # Define Variables for Template Creation
    resrc_desc = 'inb_mgmt_default_epg'
    class_name = 'mgmtInB'
    dn_strings = 'uni/tn-mgmt/mgmtp-default/inb-inb_epg'
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)
    descrption = 'Default Inband Mmgmt EPG Used by Brahma Startup Wizard.'
    encapsulat = 'vlan-{}'.format(inb_vlan)
    childclass = 'mgmtRsMgmtBD'
    child_Brdg = 'inb'

    base_atts = {'dn': dn_strings, 'descr': descrption, 'encap': encapsulat, 'name': 'inb_epg'}
    child_atts = {'tnFvBDName': child_Brdg}
    data_out = {class_name: {'attributes': base_atts, 'children': [{childclass: {'attributes': child_atts}}]}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

    # Close the File created for this resource
    wr_file.close()

def resource_ntp(ntp_ipv4, prefer, mgmt_domain):
    # Validate Management Domain
    mgmt_epg = validating.mgmt_domain(line_count, mgmt_domain)
    
    # Validate NTP IPv4 Address
    try:
        validating.ipv4(line_count, ntp_ipv4)
    except Exception as err:
        print('\r\r----------------\r')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}, Please verify {ntp_ipv4} input information.')
        print('----------------\r\r')
        exit()

    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation
    ntp_ipv4_ = ntp_ipv4.replace('.', '_')
    resrc_desc = 'ntp_{}'.format(ntp_ipv4_)
    class_name = 'datetimeNtpProv'
    rn_strings = "ntpprov-{}".format(ntp_ipv4)
    dn_strings = "uni/fabric/time-default/{}".format(rn_strings)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)
    childclass = 'datetimeRsNtpProvToEpg'
    child_tDn = 'uni/tn-mgmt/mgmtp-default/{}'.format(mgmt_epg)

    base_atts = {'dn': dn_strings, 'name': ntp_ipv4, 'preferred': prefer, 'rn': rn_strings}
    child_atts = {'tDn': child_tDn}
    data_out = {class_name: {'attributes': base_atts, 'children': [{childclass: {'attributes': child_atts}}]}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

def resource_SmarthCallHome(smtp_port, smtp_relay, mgmt_domain, ch_fr_email, ch_rp_email, ch_to_email, phone_numbr, contact_inf,
                            str_address, contract_id, customer_id, site_identi):
    
    # Translate recieved import for mgpt_epg format
    mgmt_epg = validating.mgmt_domain(line_count, mgmt_domain)

    # Validate All the Email Addresses
    validating.email(line_count, ch_fr_email)
    validating.email(line_count, ch_rp_email)
    validating.email(line_count, ch_to_email)

    # Validate Phone Number
    validating.phone(line_count, phone_numbr)

    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation
    resrc_desc = 'SmartCallHome_dg'
    class_name = 'callhomeSmartGroup'
    rn_strings = "smartgroup-SmartCallHome_dg"
    dn_strings = "uni/fabric/{}".format(rn_strings)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)
    name = 'SmartCallHome_dg'
    
    child_1_class = 'callhomeProf'
    child_1_Rn = 'prof'
    child_1_Dn = 'uni/fabric/smartgroup-SmartCallHome_dg/{}'.format(child_1_Rn)

    sub_child_class = 'callhomeSmtpServer'
    sub_child_Rn = 'smtp'
    sub_child_Dn = 'uni/fabric/smartgroup-SmartCallHome_dg/prof/{}'.format(sub_child_Rn)

    basement_class = 'fileRsARemoteHostToEpg'
    basement_tDn = 'uni/tn-mgmt/mgmtp-default/{}'.format(mgmt_epg)


    child_2_class = 'callhomeSmartDest'
    child_2_Rn = 'smartdest-SCH_Receiver'
    child_2_Dn = 'uni/fabric/smartgroup-SmartCallHome_dg/{}'.format(child_2_Rn)

    base_atts = {'dn': dn_strings, 'name': name, 'rn': rn_strings}
    basement_child = {basement_class: {'attributes': {'tDn': basement_tDn}, 'children': []}}
    sub_child = {sub_child_class: {'attributes': {'dn': sub_child_Dn, 'host': smtp_relay, 'rn': sub_child_Rn}, 'children': [basement_child]}}
    child_1_atts = {child_1_class: {'attributes': {'dn': child_1_Dn, 'port': smtp_port, 'from': ch_fr_email, 'replyTo': ch_rp_email,
                    'email': ch_to_email, 'phone': phone_numbr, 'contact': contact_inf, 'addr': str_address, 'contract': contract_id,
                    'customer': customer_id, 'site': site_identi, 'rn': child_1_Rn}, 'children': [sub_child]}}
    child_2_atts = {child_2_class: {'attributes': {'dn': child_2_Dn, 'name': 'SCH_Receiver', 'email': ch_to_email,
                    'format': 'short-txt', 'rn': child_2_Rn}, 'children': []}}

    child_combined = [child_1_atts, child_2_atts]
    data_out = {class_name: {'attributes': base_atts, 'children': child_combined}}
    
    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)


    # Define Variables for Template Creation
    resrc_desc = 'callhomeSmartSrc'
    class_name = 'callhomeSmartSrc'
    rn_strings = "smartchsrc"
    dn_strings = "uni/infra/moninfra-default/{}".format(rn_strings)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)
    name = 'SmartCallHome_dg'
    
    child_1_class = 'callhomeRsSmartdestGroup'
    child_1_tDn = 'uni/fabric/smartgroup-SmartCallHome_dg'

    base_atts = {'dn': dn_strings, 'rn': rn_strings}
    child_1_atts = {child_1_class: {'attributes': {'tDn': child_1_tDn}, 'children': []}}

    child_combined = [child_1_atts]
    data_out = {class_name: {'attributes': base_atts, 'children': child_combined}}
    
    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

def resource_snmp_client(client_name, client_ipv4, mgmt_domain):
    # Validate Management Domain
    snmp_mgmt = validating.snmp_mgmt(line_count, mgmt_domain)
    
    # Validate SNMP IPv4 Client Address
    try:
        validating.ipv4(line_count, client_ipv4)
    except Exception as err:
        print('\r\r----------------\r')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}, Please verify {client_ipv4} input information.')
        print('----------------\r\r')
        exit()

    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation
    client_ipv4_ = client_ipv4.replace('.', '_')
    resrc_desc = 'snmp_client_{}'.format(client_ipv4_)
    class_name = 'snmpClientP'
    rn_strings = "client-{}".format(client_ipv4)
    dn_strings = "uni/fabric/snmppol-default/clgrp-{}_Clients/client-[{}]".format(snmp_mgmt, client_ipv4)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)

    base_atts = {'dn': dn_strings, 'name': client_name, 'addr': client_ipv4, 'rn': rn_strings}
    data_out = {class_name: {'attributes': base_atts, 'children': []}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

def resource_snmp_comm(community, description):
    # Validate SNMP Community
    validating.snmp_string(line_count, community)

    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation
    resrc_desc = 'snmp_comm_{}'.format(community)
    class_name = 'snmpCommunityP'
    rn_strings = "community-{}".format(community)
    dn_strings = "uni/fabric/snmppol-default/{}".format(rn_strings)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)

    base_atts = {'dn': dn_strings, 'descr': description, 'name': community, 'rn': rn_strings}
    data_out = {class_name: {'attributes': base_atts, 'children': []}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

    wr_comm.write('%s\n' % (community))

def resource_snmp_info(contact, location):
    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation
    resrc_desc = 'snmp_info'
    class_name = 'snmpPol'
    dn_strings = "uni/fabric/snmppol-default"
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)
    descrption = 'This is the default SNMP Policy'

    base_atts = {'dn': dn_strings, 'descr': descrption, 'adminSt': 'enabled', 'contact': contact, 'loc': location}
    data_out = {class_name: {'attributes': base_atts, 'children': []}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

def resource_snmp_trap(snmp_ipv4, snmp_port, snmp_vers, snmp_string, snmp_auth, mgmt_domain):
    
    # Validate SNMP Trap Server IPv4 Address
    try:
        validating.ipv4(line_count, snmp_ipv4)
    except Exception as err:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}, Please verify {snmp_ipv4} input information.\n')
        print(f'-----------------------------------------------------------------------------\n')
        exit()

    # Validate SNMP Port
    validating.port(line_count, snmp_port)

    # Check SNMP Version
    if not re.search('(v1|v2c|v3)', snmp_vers):
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'  Error on Row {line_count}. SNMP Version {snmp_vers} is not valid.')
        print(f'  Valid SNMP versions are [v1|v2c|v3].  Exiting....\n')
        print(f'------------------------------------------------------------------------------\n')
        exit()

    # Set noauth if v1 or v2c
    if re.search('(v1|v2c)', snmp_vers):
        snmp_auth = 'noauth'
    
    # Validate SNMP Community or Username
    validating.snmp_string(line_count, snmp_string)

    # Validate Management Domain
    mgmt_epg = validating.mgmt_domain(line_count, mgmt_domain)

    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation
    snmp_ipv4_ = snmp_ipv4.replace('.', '_')
    resrc_desc = 'snmp_trap_default_{}'.format(snmp_ipv4_)
    class_name = 'snmpTrapFwdServerP'
    dn_strings = "uni/fabric/snmppol-default/trapfwdserver-[{}]".format(snmp_ipv4)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)
    
    if snmp_port == '':
        base_atts = {'dn': dn_strings, 'addr': snmp_ipv4,}
    else:
        base_atts = {'dn': dn_strings, 'addr': snmp_ipv4, 'port': snmp_port}
    data_out = {class_name: {'attributes': base_atts, 'children': []}}
    
    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)
    
    # Define Variables for Template Creation
    resrc_desc = 'snmp_trap_dest_{}'.format(snmp_ipv4_)
    class_name = 'snmpGroup'
    rn_strings = "snmpgroup-SNMP-TRAP_dg"
    dn_strings = "uni/fabric/{}".format(rn_strings)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)
    descrption = 'SNMP Trap Destination Group - Created by Brahma Startup Script'
    name = 'SNMP-TRAP_dg'
    
    childclass = 'snmpTrapDest'
    child_Rn = 'trapdest-{}-port-{}'.format(snmp_ipv4, snmp_port)
    child_Dn = 'uni/fabric/snmpgroup-SNMP-TRAP_dg/{}'.format(child_Rn)
    
    sub_child_class = 'fileRsARemoteHostToEpg'
    sub_child_tDn = 'uni/tn-mgmt/mgmtp-default/{}'.format(mgmt_epg)
    
    base_atts = {'dn': dn_strings, 'descr': descrption, 'name': name, 'rn': rn_strings}
    sub_child = {sub_child_class: {'attributes': {'tDn': sub_child_tDn}}}
    child_atts = {childclass: {'attributes': {'dn': child_Dn, 'ver': snmp_vers, 'host': snmp_ipv4, 'port': snmp_port,
                  'secName': snmp_string, 'v3SecLvl': snmp_auth, 'rn': child_Rn}, 'children': [sub_child]}}
    child_combined = [child_atts]
    data_out = {class_name: {'attributes': base_atts, 'children': child_combined}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

def resource_snmp_user(snmp_user, priv_type, priv_key, auth_type, auth_key):
    if not (priv_type == 'none' or priv_type == 'aes-128' or priv_type == 'des'):
        print(f"----------------\r")
        print(f"  Error on Row {line_count}. priv_type {priv_type} is not ")
        print(f"  'none', 'des', or 'aes-128'.  Exiting....")
        print("----------------")
        exit()
    if not priv_type == 'none':
        if not validators.length(priv_key, min=8):
            print(f"----------------\r")
            print(f"  Error on Row {line_count}. priv_key does not ")
            print(f"  meet the minimum character count of 8.  Exiting....")
            print("----------------")
            exit()

    if not validators.length(auth_key, min=8):
        print(f"----------------\r")
        print(f"  Error on Row {line_count}. auth_key does not ")
        print(f"  meet the minimum character count of 8.  Exiting....")
        print("----------------")
        exit()

    if priv_type == 'none':
        priv_type = ''
    if auth_type == 'md5':
        auth_type = ''
    if auth_type == 'sha1':
        auth_type = 'hmac-sha1-96'
    
    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation
    resrc_desc = 'snmp_user_{}'.format(snmp_user)
    class_name = 'snmpUserP'
    dn_strings = "uni/fabric/snmppol-default/user-{}".format(snmp_user)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)

    if not priv_type == '':
        if not auth_type == '':
            base_atts = {'dn': dn_strings, 'name': snmp_user, 'privType': priv_type, 'privKey': priv_key, 
                         'authType': auth_type, 'authKey': auth_key,}
        else:
            base_atts = {'dn': dn_strings, 'name': snmp_user, 'privType': priv_type, 'privKey': priv_key, 
                         'authKey': auth_key,}
    elif not auth_type == '':
        base_atts = {'dn': dn_strings, 'name': snmp_user, 'authType': auth_type, 'authKey': auth_key}
    else:
        base_atts = {'dn': dn_strings, 'name': snmp_user, 'authKey': auth_key}
        
    data_out = {class_name: {'attributes': base_atts, 'children': []}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

def resource_switch(serial, name, node_id, node_type, pod_id, switch_role, modules, port_count, oob_ipv4, oob_gwv4, inb_ipv4, inb_gwv4, inb_vlan):
    try:
        # Validate Serial Number
        
        # Validate Hostname
        validating.hostname(line_count, name)
        
        # Validate Node_ID
        validating.node_id(line_count, node_id)

        # Validate node_type
        validating.node_type(line_count, name, node_type)

        # Validate Pod_ID
        validating.pod_id(line_count, name, pod_id)

        # Validate switch role
        validating.role(line_count, name, switch_role)

        # Validate Modules
        validating.modules(line_count, name, switch_role, modules)

        # Validate port_count
        validating.port_count(line_count, name, switch_role, port_count)

        # Validate InBand Network
        validating.inband(line_count, name, inb_ipv4, inb_gwv4)

        # Validate Out-of-Band Network
        validating.oob(line_count, name, oob_ipv4, oob_gwv4)

    except Exception as err:
        print('\r\r----------------\r')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}, Please verify input information.')
        print('----------------\r\r')
        exit()
    pod_id = str(pod_id)
    file_sw = ('resources_user_import_xDevice_%s.tf' % (name))
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
    wr_file_sw.write('# role: spine, leaf.\n')
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
    wr_file_sw.write('\tpath       = "/api/node/mo/uni/tn-mgmt.json"\n')
    wr_file_sw.write('\tclass_name = "mgmtRsOoBStNode"\n')
    wr_file_sw.write('\tpayload    = <<EOF\n')
    wr_file_sw.write('{\n')
    wr_file_sw.write('\t"mgmtRsOoBStNode": {\n')
    wr_file_sw.write('\t\t"attributes": {\n')
    wr_file_sw.write('\t\t\t"addr": "%s",\n' % (oob_ipv4))
    wr_file_sw.write('\t\t\t"dn": "uni/tn-mgmt/mgmtp-default/oob-default/rsooBStNode-[topology/pod-%s/node-%s]",\n' % (pod_id, node_id))
    wr_file_sw.write('\t\t\t"gw": "%s",\n' % (oob_gwv4))
    wr_file_sw.write('\t\t\t"tDn": "topology/pod-%s/node-%s",\n' % (pod_id, node_id))
    wr_file_sw.write('\t\t\t"v6Addr": "::",\n')
    wr_file_sw.write('\t\t\t"v6Gw": "::"\n')
    wr_file_sw.write('\t\t}\n')
    wr_file_sw.write('\t}\n')
    wr_file_sw.write('}\n')
    wr_file_sw.write('\tEOF\n')
    wr_file_sw.write('}\n')
    wr_file_sw.write('\n')
    wr_file_sw.write('resource "aci_rest" "inb_mgmt_%s" {\n' % (name))
    wr_file_sw.write('\tpath       = "/api/node/mo/uni/tn-mgmt.json"\n')
    wr_file_sw.write('\tclass_name = "mgmtRsInBStNode"\n')
    wr_file_sw.write('\tpayload    = <<EOF\n')
    wr_file_sw.write('{\n')
    wr_file_sw.write('\t"mgmtRsInBStNode": {\n')
    wr_file_sw.write('\t\t"attributes": {\n')
    wr_file_sw.write('\t\t\t"addr": "%s",\n' % (inb_ipv4))
    wr_file_sw.write('\t\t\t"dn": "uni/tn-mgmt/mgmtp-default/inb-inb_epg/rsinBStNode-[topology/pod-%s/node-%s]",\n' % (pod_id, node_id))
    wr_file_sw.write('\t\t\t"gw": "%s",\n' % (inb_gwv4))
    wr_file_sw.write('\t\t\t"tDn": "topology/pod-%s/node-%s",\n' % (pod_id, node_id))
    wr_file_sw.write('\t\t}\n')
    wr_file_sw.write('\t}\n')
    wr_file_sw.write('}\n')
    wr_file_sw.write('\tEOF\n')
    wr_file_sw.write('}\n')
    wr_file_sw.write('\n')
    node_id = int(node_id)
    if node_id % 2 == 0:
        fwg = 'switch_MgB'
    else:
        fwg = 'switch_MgA'
    # wr_file_sw.write('resource "aci_node_block_firmware" "%s" {\n' % (name))
    # wr_file_sw.write('\tfirmware_group_dn = "uni/fabric/fwgrp-%s"\n' % (fwg))
    # wr_file_sw.write('\tname              = "nodeblk-blk%s-%s"\n' % (node_id, node_id))
    # wr_file_sw.write('\tfrom_             = "%s"\n' % (node_id))
    # wr_file_sw.write('\tto_               = "%s"\n' % (node_id))
    # wr_file_sw.write('}\n')
    # wr_file_sw.write('\n')
    wr_file_sw.write('resource "aci_rest" "maint_grp_%s" {\n' % (name))
    wr_file_sw.write('\tpath       = "/api/node/mo/uni/fabric/maintgrp-%s.json"\n'% (fwg))
    wr_file_sw.write('\tclass_name = "maintMaintGrp"\n')
    wr_file_sw.write('\tpayload    = <<EOF\n')
    wr_file_sw.write('{\n')
    wr_file_sw.write('\t"maintMaintGrp": {\n')
    wr_file_sw.write('\t\t"attributes": {\n')
    wr_file_sw.write('\t\t\t"dn": "uni/fabric/maintgrp-%s"' % (fwg))
    wr_file_sw.write('\t\t},\n')
    wr_file_sw.write('\t\t"children": [\n')
    wr_file_sw.write('\t\t\t{\n')
    wr_file_sw.write('\t\t\t\t"fabricNodeBlk": {\n')
    wr_file_sw.write('\t\t\t\t\t"attributes": {\n')
    wr_file_sw.write('\t\t\t\t\t\t"dn": "uni/fabric/maintgrp-%s/nodeblk-blk%s-%s",\n'% (fwg, node_id, node_id))
    wr_file_sw.write('\t\t\t\t\t\t"name": "blk%s-%s",\n' % (node_id, node_id))
    wr_file_sw.write('\t\t\t\t\t\t"from_": "%s",\n' % (node_id))
    wr_file_sw.write('\t\t\t\t\t\t"to_": "%s",\n' % (node_id))
    wr_file_sw.write('\t\t\t\t\t\t"rn": "nodeblk-blk%s-%s"\n' % (node_id, node_id))
    wr_file_sw.write('\t\t\t\t\t}\n')
    wr_file_sw.write('\t\t\t\t}\n')
    wr_file_sw.write('\t\t\t}\n')
    wr_file_sw.write('\t\t]\n')
    wr_file_sw.write('\t\t}\n')
    wr_file_sw.write('\t}\n')
    wr_file_sw.write('}\n')
    wr_file_sw.write('\tEOF\n')
    wr_file_sw.write('}\n')
    wr_file_sw.write('\n')

    if switch_role == 'leaf':
        wr_file_sw.write('resource "aci_leaf_profile" "%s_SwSel" {\n' % (name))
        wr_file_sw.write('\tname = "%s_SwSel"\n' % (name))
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
        wr_file_sw.write('resource "aci_leaf_interface_profile" "%s_IntProf" {\n' % (name))
        wr_file_sw.write('\tname = "%s_IntProf"\n' % (name))
        wr_file_sw.write('}\n')
        wr_file_sw.write('\n')
        wr_file_sw.write('resource "aci_rest" "leaf_int_selector_%s_IntProf" {\n' % (name))
        wr_file_sw.write('\tpath       = "/api/node/mo/uni/infra/nprof-%s_SwSel.json"\n' % (name))
        wr_file_sw.write('\tclass_name = "infraRsAccPortP"\n')
        wr_file_sw.write('\tpayload    = <<EOF\n')
        wr_file_sw.write('{\n')
        wr_file_sw.write('\t"infraRsAccPortP": {\n')
        wr_file_sw.write('\t\t"attributes": {\n')
        wr_file_sw.write('\t\t\t"tDn": "uni/infra/accportprof-%s_IntProf"\n' % (name))
        wr_file_sw.write('\t\t}\n')
        wr_file_sw.write('\t}\n')
        wr_file_sw.write('}\n')
        wr_file_sw.write('\tEOF\n')
        wr_file_sw.write('}\n')
        wr_file_sw.write('\n')
        mod_count = 0
        while mod_count < int(modules):
            mod_count += 1
            wr_file_sw.write('resource "aci_rest" "%s_%s_IntProf" {\n' % (name, mod_count))
            wr_file_sw.write('\tfor_each         = var.port-selector-%s\n' %(port_count))
            wr_file_sw.write('\tpath             = "/api/node/mo/uni/infra/accportprof-%s_IntProf/hports-Eth%s-${each.value.name}-typ-range.json"\n' % (name, mod_count))
            wr_file_sw.write('\tclass_name       = "infraHPortS"\n')
            wr_file_sw.write('\tpayload          = <<EOF\n')
            wr_file_sw.write('{\n')
            wr_file_sw.write('\t"infraHPortS": {\n')
            wr_file_sw.write('\t\t"attributes": {\n')
            wr_file_sw.write('\t\t\t"dn": "uni/infra/accportprof-%s_IntProf/hports-Eth%s-${each.value.name}-typ-range",\n' % (name, mod_count))
            wr_file_sw.write('\t\t\t"name": "Eth%s-${each.value.name}",\n' % (mod_count))
            wr_file_sw.write('\t\t\t"rn": "hports-Eth%s-${each.value.name}-typ-range"\n' % (mod_count))
            wr_file_sw.write('\t\t},\n')
            wr_file_sw.write('\t\t"children": [\n')
            wr_file_sw.write('\t\t\t{\n')
            wr_file_sw.write('\t\t\t\t"infraPortBlk": {\n')
            wr_file_sw.write('\t\t\t\t\t"attributes": {\n')
            wr_file_sw.write('\t\t\t\t\t\t"dn": "uni/infra/accportprof-%s_IntProf/hports-Eth%s-${each.value.name}-typ-range/portblk-block2",\n' % (name, mod_count))
            wr_file_sw.write('\t\t\t\t\t\t"fromCard": "%s",\n' % (mod_count))
            wr_file_sw.write('\t\t\t\t\t\t"fromPort": "${each.value.name}",\n')
            wr_file_sw.write('\t\t\t\t\t\t"toCard": "%s",\n' % (mod_count))
            wr_file_sw.write('\t\t\t\t\t\t"toPort": "${each.value.name}",\n')
            wr_file_sw.write('\t\t\t\t\t\t"name": "block2",\n')
            wr_file_sw.write('\t\t\t\t\t\t"rn": "portblk-block2"\n')
            wr_file_sw.write('\t\t\t\t\t}\n')
            wr_file_sw.write('\t\t\t\t}\n')
            wr_file_sw.write('\t\t\t}\n')
            wr_file_sw.write('\t\t]\n')
            wr_file_sw.write('\t}\n')
            wr_file_sw.write('}\n')
            wr_file_sw.write('\tEOF\n')
            wr_file_sw.write('}\n')
            wr_file_sw.write('\n')
    elif switch_role == 'spine':
        wr_file_sw.write('resource "aci_spine_profile" "%s_SwSel" {\n' % (name))
        wr_file_sw.write('\tname = "%s_SwSel"\n' % (name))
        wr_file_sw.write('}\n')
        wr_file_sw.write('\n')
        wr_file_sw.write('resource "aci_spine_interface_profile" "%s_IntProf" {\n' % (name))
        wr_file_sw.write('\tname = "%s_IntProf"\n' % (name))
        wr_file_sw.write('}\n')
        wr_file_sw.write('\n')
        wr_file_sw.write('resource "aci_spine_port_policy_group" "%s" {\n' % (name))
        wr_file_sw.write('\tname = "%s"\n' % (name))
        wr_file_sw.write('}\n')
        wr_file_sw.write('\n')
        wr_file_sw.write('resource "aci_spine_switch_association" "%s" {\n' % (name))
        wr_file_sw.write('\t\tspine_profile_dn              = aci_spine_profile.%s_SwSel.id\n' % (name))
        wr_file_sw.write('\t\tname                          = "%s"\n' % (name))
        wr_file_sw.write('\t\tspine_switch_association_type = "range"\n')
        wr_file_sw.write('}\n')
        wr_file_sw.write('\n')
        wr_file_sw.write('resource "aci_spine_port_selector" "%s" {\n' % (name))
        wr_file_sw.write('\t\tspine_profile_dn              = aci_spine_profile.%s_SwSel.id\n' % (name))
        wr_file_sw.write('\t\ttdn                           = aci_spine_interface_profile.%s_IntProf.id\n' % (name))
        wr_file_sw.write('}\n')
        wr_file_sw.write('\n')
        mod_count = 0
        while mod_count < int(modules):
            mod_count += 1
            wr_file_sw.write('resource "aci_rest" "%s_%s_IntProf" {\n' % (name, mod_count))
            wr_file_sw.write('\tfor_each         = var.port-selector-%s\n' %(port_count))
            wr_file_sw.write('\tpath             = "/api/node/mo/uni/infra/spaccportprof-%s_IntProf/shports-Eth%s-${each.value.name}-typ-range.json"\n' % (name, mod_count))
            wr_file_sw.write('\tclass_name       = "infraSHPortS"\n')
            wr_file_sw.write('\tpayload          = <<EOF\n')
            wr_file_sw.write('{\n')
            wr_file_sw.write('\t"infraSHPortS": {\n')
            wr_file_sw.write('\t\t"attributes": {\n')
            wr_file_sw.write('\t\t\t"dn": "uni/infra/spaccportprof-%s_IntProf/shports-Eth%s-${each.value.name}-typ-range",\n' % (name, mod_count))
            wr_file_sw.write('\t\t\t"name": "Eth%s-${each.value.name}",\n' % (mod_count))
            wr_file_sw.write('\t\t\t"rn": "shports-Eth%s-${each.value.name}-typ-range"\n' % (mod_count))
            wr_file_sw.write('\t\t},\n')
            wr_file_sw.write('\t\t"children": [\n')
            wr_file_sw.write('\t\t\t{\n')
            wr_file_sw.write('\t\t\t\t"infraPortBlk": {\n')
            wr_file_sw.write('\t\t\t\t\t"attributes": {\n')
            wr_file_sw.write('\t\t\t\t\t\t"dn": "uni/infra/spaccportprof-%s_IntProf/shports-Eth%s-${each.value.name}-typ-range/portblk-block2",\n' % (name, mod_count))
            wr_file_sw.write('\t\t\t\t\t\t"fromCard": "%s",\n' % (mod_count))
            wr_file_sw.write('\t\t\t\t\t\t"fromPort": "${each.value.name}",\n')
            wr_file_sw.write('\t\t\t\t\t\t"toCard": "%s",\n' % (mod_count))
            wr_file_sw.write('\t\t\t\t\t\t"toPort": "${each.value.name}",\n')
            wr_file_sw.write('\t\t\t\t\t\t"name": "block2",\n')
            wr_file_sw.write('\t\t\t\t\t\t"rn": "portblk-block2"\n')
            wr_file_sw.write('\t\t\t\t\t}\n')
            wr_file_sw.write('\t\t\t\t}\n')
            wr_file_sw.write('\t\t\t}\n')
            wr_file_sw.write('\t\t]\n')
            wr_file_sw.write('\t}\n')
            wr_file_sw.write('}\n')
            wr_file_sw.write('\tEOF\n')
            wr_file_sw.write('}\n')
            wr_file_sw.write('\n')
    wr_file_sw.close()

def resource_syslog(syslog_ipv4, syslog_port, mgmt_domain, severity, facility, local_state, local_level, console_state, console_level):
    # Validate Syslog Server IPv4 Address
    try:
        validating.ipv4(line_count, syslog_ipv4)
    except Exception as err:
        print('\r\r----------------\r')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}, Please verify Syslog IP {syslog_ipv4} information.')
        print('----------------\r\r')
        exit()

    # Validate Syslog Port
    validating.port(line_count, syslog_port)

    # Validate Management Domain
    mgmt_epg = validating.mgmt_domain(line_count, mgmt_domain)

    # Validate Syslog Facility
    if not re.match("local[0-7]", facility):
        print('\n----------------\n')
        print(f'   Error on Row {line_count}, Please verify Syslog Facility {facility}.\n')
        print('----------------\n')
        exit()

    # Validate Syslog Levels
    validating.log_level(line_count, 'remote', severity)
    validating.log_level(line_count, 'local', local_level)
    validating.log_level(line_count, 'console', console_level)

    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation
    syslog_ipv4_ = syslog_ipv4.replace('.', '_')
    resrc_desc = 'syslog_{}'.format(syslog_ipv4_)
    class_name = 'syslogGroup'
    rn_strings = "slgroup-Syslog-dg_{}".format(syslog_ipv4)
    dn_strings = "uni/fabric/{}".format(rn_strings)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)
    descrption = 'Syslog Destination Group {} - Created by Brahma Startup Wizard'.format(syslog_ipv4)
    name = 'Syslog-dg_{}'.format(syslog_ipv4)
    
    child_1_class = 'syslogConsole'
    child_1_Rn = 'console'
    child_1_Dn = 'uni/fabric/slgroup-Syslog-dg_{}/{}'.format(syslog_ipv4, child_1_Rn)
    child_1_sv = '{}'.format(console_level)
    child_1_state = '{}'.format(console_state)
    child_2_class = 'syslogFile'
    child_2_Rn = 'file'
    child_2_Dn = 'uni/fabric/slgroup-Syslog-dg_{}/{}'.format(syslog_ipv4, child_2_Rn)
    child_2_sv = '{}'.format(local_level)
    child_2_state = '{}'.format(local_state)
    child_3_class = 'syslogProf'
    child_3_Rn = 'prof'
    child_3_Dn = 'uni/fabric/slgroup-Syslog-dg_{}/{}'.format(syslog_ipv4, child_3_Rn)
    child_3_state = '{}'.format(local_state)
    child_4_class = 'syslogRemoteDest'
    child_4_Rn = 'rdst-{}'.format(syslog_ipv4)
    child_4_Dn = 'uni/fabric/slgroup-Syslog-dg_{}/{}'.format(syslog_ipv4, child_4_Rn)
    child_4_sv = '{}'.format(severity)
    child_4_fwdf = '{}'.format(facility)
    child_4_host = '{}'.format(syslog_ipv4)
    child_4_name = 'RmtDst-{}'.format(syslog_ipv4)
    child_4_port = '{}'.format(syslog_port)
    child_4_state = 'enabled'
    sub_child_class = 'fileRsARemoteHostToEpg'
    sub_child_tDn = 'uni/tn-mgmt/mgmtp-default/{}'.format(mgmt_epg)
    
    
    base_atts = {'dn': dn_strings, 'includeMilliSeconds': 'true', 'includeTimeZone': 'true', 'descr': descrption, 'name': name, 'rn': rn_strings}
    child_1_atts = {child_1_class: {'attributes': {'dn': child_1_Dn, 'adminState': child_1_state, 'severity': child_1_sv, 'rn': child_1_Rn}, 'children': []}}
    child_2_atts = {child_2_class: {'attributes': {'dn': child_2_Dn, 'adminState': child_2_state, 'severity': child_2_sv, 'rn': child_2_Rn}, 'children': []}}
    child_3_atts = {child_3_class: {'attributes': {'dn': child_3_Dn, 'adminState': child_3_state, 'rn': child_3_Rn}, 'children': []}}
    sub_child = {sub_child_class: {'attributes': {'tDn': sub_child_tDn}, 'children': []}}
    child_4_atts = {child_4_class: {'attributes': {'dn': child_4_Dn, 'host': child_4_host, 'name': child_4_name, 'adminState': child_4_state, 
                    'forwardingFacility': child_4_fwdf, 'port': child_4_port,'severity': child_4_sv, 'rn': child_4_Rn}, 'children': [sub_child]}}

    child_combined = [child_1_atts, child_2_atts, child_3_atts, child_4_atts]
    data_out = {class_name: {'attributes': base_atts, 'children': child_combined}}
    
    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

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
                resource_apic_inb(name, node_id, pod_id, inb_ipv4, inb_gwv4, inb_vlan, p1_leaf, p1_swpt, p2_leaf, p2_swpt)
                if count_inb_gwv4 == 0: 
                    resource_inband(inb_ipv4, inb_gwv4, inb_vlan)
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
                resource_bgp_as(bgp_as)
                line_count += 1
            elif type == 'bgp_rr':
                node_id = column[2]
                # Configure the Default BGP Route Reflector
                resource_bgp_rr(node_id)
                line_count += 1
            elif type == 'dns':
                dns_ipv4 = column[1]
                prefer = column[2]
                if count_dns_servers < 2:
                    # Create Resource Record for DNS Servers
                    resource_dns(dns_ipv4, prefer) 
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
                resource_dns_mgmt(mgmt_domain) 
                line_count += 1
            elif type == 'search_domain':
                domain = column[1]
                prefer = column[2]
                # Create Resource Record for Search Domain
                resource_domain(domain, prefer) 
                line_count += 1
            elif type == 'inband_vlan':
                inb_vlan = column[1]
                line_count += 1
            elif type == 'ntp':
                ntp_ipv4 = column[1]
                prefer = column[2]
                mgmt_domain = column[3]
                # Create Resource Record for NTP Servers
                resource_ntp(ntp_ipv4, prefer, mgmt_domain)
                line_count += 1
            elif type == 'smartcallhome':
                smtp___port = column[1]
                smtp__relay = column[2]
                mgmt_domain = column[3]
                ch_fr_email = column[4]
                ch_rp_email = column[5]
                ch_to_email = column[6]
                phone_numbr = column[7]
                contact_inf = column[8]
                str_address = column[9]
                contract_id = column[10]
                customer_id = column[11]
                site_identi = column[12]
                # Configure the Default SmartCallHome Policy
                resource_SmarthCallHome(smtp___port, smtp__relay, mgmt_domain, ch_fr_email, ch_rp_email, ch_to_email, phone_numbr, 
                                        contact_inf, str_address, contract_id, customer_id, site_identi)
                line_count += 1
            elif type == 'snmp_client':
                client_name = column[1]
                client_ipv4 = column[2]
                mgmt_domain = column[3]
                # Create Resource Record for SNMP Client
                resource_snmp_client(client_name, client_ipv4, mgmt_domain)
                line_count += 1
            elif type == 'snmp_comm':
                community = column[1]
                description = column[2]
                # Create Resource Record for SNMP Communities
                resource_snmp_comm(community, description)
                line_count += 1
            elif type == 'snmp_info':
                contact = column[1]
                location = column[2]
                # Create Resource Record for SNMP Default Policy
                resource_snmp_info(contact, location)
                line_count += 1
            elif type == 'snmp_trap':
                snmp_ipv4 = column[1]
                snmp_port = column[2]
                snmp_vers = column[3]
                snmp_string = column[4]
                snmp_auth = column[5]
                mgmt_domain = column[6]
                # Create Resource Record for SNMP Traps
                resource_snmp_trap(snmp_ipv4, snmp_port, snmp_vers, snmp_string, snmp_auth, mgmt_domain)
                line_count += 1
            elif type == 'snmp_user':
                snmp_user = column[1]
                priv_type = column[2]
                priv_key = column[3]
                auth_type = column[4]
                auth_key = column[5]
                # Create Resource Record for SNMP Users
                resource_snmp_user(snmp_user, priv_type, priv_key, auth_type, auth_key)
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
                resource_switch(serial, name, node_id, node_type, pod_id, switch_role, modules, port_count, oob_ipv4, oob_gwv4, 
                                inb_ipv4, inb_gwv4, inb_vlan)
                if count_inb_gwv4 == 0: 
                    resource_inband(inb_ipv4, inb_gwv4, inb_vlan)
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
            elif type == 'syslog':
                syslog_ipv4 = column[1]
                syslog_port = column[2]
                mgmt_domain = column[3]
                severity = column[4]
                facility = column[5]
                local_state = column[6]
                local_level = column[7]
                console_state = column[8]
                console_level = column[9]
                resource_syslog(syslog_ipv4, syslog_port, mgmt_domain, severity, facility, local_state, local_level, console_state, console_level)
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
wr_vrfs.close()
wr_comm.close()

comm_uniq = 'cp snmp_comms.txt snmp_comms1.txt ; cat snmp_comms1.txt | sort | uniq > snmp_comms.txt ; rm snmp_comms1.txt'
vrfs_cmds = 'cp vrfs.txt vrfs1.txt ; cat vrfs1.txt | sort | uniq > vrfs.txt ; rm vrfs1.txt'
os.system(comm_uniq)
os.system(vrfs_cmds)

file_comm = open(file_comm, 'r')
file_vrfs = open(file_vrfs, 'r')

if not os.stat('snmp_comms.txt').st_size == 0:
    file_snmp_ctx_cmds = 'resources_user_Tenant_SNMP_Ctx.tf'
    file_snmp_ctx_vars = 'variables_user_Tenant_SNMP_Ctx.tf'
    file_snmp_ctx_comm = 'variables_user_Tenant_SNMP_Communities.tf'
    wr_snmp_ctx = open(file_snmp_ctx_cmds, 'w')
    wr_snmp_vars = open(file_snmp_ctx_vars, 'w')
    wr_snmp_comm = open(file_snmp_ctx_comm, 'w')
    wr_snmp_ctx.write('resource "aci_rest" "snmp_ctx" {\n')
    wr_snmp_ctx.write('\tfor_each        = var.snmp_ctx\n')
    wr_snmp_ctx.write('\tpath            = "/api/node/mo/uni/tn-${each.value.tenant}/ctx-${each.value.ctx}/snmpctx.json"\n')
    wr_snmp_ctx.write('\tclass_name      = "vzOOBBrCP"\n')
    wr_snmp_ctx.write('\tpayload         = <<EOF\n')
    wr_snmp_ctx.write('{\n')
    wr_snmp_ctx.write('\t"snmpCtxP": {\n')
    wr_snmp_ctx.write('\t\t"attributes": {\n')
    wr_snmp_ctx.write('\t\t\t"dn": "uni/tn-${each.value.tenant}/ctx-${each.value.ctx}/snmpctx",\n')
    wr_snmp_ctx.write('\t\t\t"name": "${each.value.name}",\n')
    wr_snmp_ctx.write('\t\t\t"rn": "snmpctx",\n')
    wr_snmp_ctx.write('\t\t},\n')
    wr_snmp_ctx.write('\t\t"children": []\n')
    wr_snmp_ctx.write('\t}\n')
    wr_snmp_ctx.write('}\n')
    wr_snmp_ctx.write('\tEOF\n')
    wr_snmp_ctx.write('}\n')
    wr_snmp_ctx.write('\n')
    wr_snmp_ctx.write('resource "aci_rest" "snmp_ctx_community" {\n')
    wr_snmp_ctx.write('\tfor_each        = var.snmp_ctx_community\n')
    wr_snmp_ctx.write('\tpath            = "/api/node/mo/uni/tn-${each.value.tenant}/ctx-${each.value.ctx}/snmpctx/community-${each.value.name}.json"\n')
    wr_snmp_ctx.write('\tclass_name      = "vzOOBBrCP"\n')
    wr_snmp_ctx.write('\tpayload         = <<EOF\n')
    wr_snmp_ctx.write('{\n')
    wr_snmp_ctx.write('\t"snmpCommunityP": {\n')
    wr_snmp_ctx.write('\t\t"attributes": {\n')
    wr_snmp_ctx.write('\t\t\t"dn": "uni/tn-${each.value.tenant}/ctx-${each.value.ctx}/snmpctx/community-${each.value.name}",\n')
    wr_snmp_ctx.write('\t\t\t"name": "${each.value.name}",\n')
    wr_snmp_ctx.write('\t\t\t"descr": "Adding Community ${each.value.name} to Ctx",\n')
    wr_snmp_ctx.write('\t\t\t"rn": "community-${each.value.name}",\n')
    wr_snmp_ctx.write('\t\t},\n')
    wr_snmp_ctx.write('\t\t"children": []\n')
    wr_snmp_ctx.write('\t}\n')
    wr_snmp_ctx.write('}\n')
    wr_snmp_ctx.write('	EOF\n')
    wr_snmp_ctx.write('}\n')
    wr_snmp_ctx.close()

    wr_snmp_vars.write('variable "snmp_ctx" {\n')
    wr_snmp_vars.write('\tdefault = {\n')
    wr_snmp_comm.write('variable "snmp_ctx_community" {\n')
    wr_snmp_comm.write('\tdefault = {\n')

    re_comm = file_comm.readlines()
    re_vrfs = file_vrfs.readlines()
    for xa in re_vrfs:
        a,b = xa.split(',')
        a = a.strip()
        b = b.strip()
        wr_snmp_vars.write('\t\t"%s_%s_ctx" = {\n' % (a, b))
        wr_snmp_vars.write('\t\t\tname        = "%s_%s_ctx"\n' % (a, b))
        wr_snmp_vars.write('\t\t\ttenant      = "%s"\n' % (a))
        wr_snmp_vars.write('\t\t\tctx         = "%s"\n' % (b))
        wr_snmp_vars.write('\t\t},\n')

        for xb in re_comm:
            xb = xb.strip()
            wr_snmp_comm.write('\t\t"%s_%s_%s" = {\n' % (a, b, xb))
            wr_snmp_comm.write('\t\t\tname        = "%s"\n' % (xb))
            wr_snmp_comm.write('\t\t\ttenant      = "%s"\n' % (a))
            wr_snmp_comm.write('\t\t\tctx         = "%s"\n' % (b))
            wr_snmp_comm.write('\t\t},\n')

    wr_snmp_vars.write('\t}\n')
    wr_snmp_vars.write('}\n')
    wr_snmp_comm.write('\t}\n')
    wr_snmp_comm.write('}\n')
    wr_snmp_vars.close()
    wr_snmp_comm.close()

#End Script
print('\r\r----------------\r')
print(f'  Completed Running Script')
print(f'  Exiting...')
print('----------------\r\r')
exit()