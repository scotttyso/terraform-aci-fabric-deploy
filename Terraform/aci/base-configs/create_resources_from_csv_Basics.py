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
    print(f'\n-----------------------------------------------------------------------------\n')
    print(f'   {csv_input} does not exist.  Exiting....')
    print(f'\n-----------------------------------------------------------------------------\n')
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

def template_aci_terraform_attr1(resrc_type, resrc_desc, attr_1st, wr_file):
    template_payload = '{0} {1}\n\t{2}\n{3}\n\n'

    resource_line = 'resource "{}" "{}"'.format(resrc_type, resrc_desc)

    wr_to_file = template_payload.format(resource_line, "{", attr_1st, "}")
    # Write Data to Template
    wr_file.write(wr_to_file)

def template_aci_terraform_attr2(resrc_type, resrc_desc, attr_1st, attr_2nd, wr_file):
    template_payload = '{0} {1}\n\t{2}\n\t{3}\n{4}\n\n'

    resource_line = 'resource "{}" "{}"'.format(resrc_type, resrc_desc)

    wr_to_file = template_payload.format(resource_line, "{", attr_1st, attr_2nd, "}")
    # Write Data to Template
    wr_file.write(wr_to_file)

def template_aci_terraform_attr3(resrc_type, resrc_desc, attr_1st, attr_2nd, attr_3rd, wr_file):
    template_payload = '{0} {1}\n\t{2}\n\t{3}\n\t{4}\n{5}\n\n'

    resource_line = 'resource "{}" "{}"'.format(resrc_type, resrc_desc)

    wr_to_file = template_payload.format(resource_line, "{", attr_1st, attr_2nd, attr_3rd, "}")
    # Write Data to Template
    wr_file.write(wr_to_file)

def resource_apic_inb(name, node_id, pod_id, inb_ipv4, inb_gwv4, inb_vlan, p1_leaf, p1_swpt, p2_leaf, p2_swpt):
    try:
        # Validate APIC Node_ID, Pod_ID, ad Inband Network
        validating.node_id_apic(line_count, name, node_id)
        validating.pod_id(line_count, name, pod_id)
        validating.inband(line_count, name, inb_ipv4, inb_gwv4)
    except Exception as err:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}.  Please verify input information.  Exiting....')
        print(f'\n-----------------------------------------------------------------------------\n')
        exit()
    
    # Convert pod_id from integer to String
    pod_id = str(pod_id)

    # Which File to Write Data to
    apic_file = 'resources_user_import_xDevice_{}.tf'.format(name)
    wr_file = open(apic_file, 'w')

    # Define Variables for Template Creation - APIC Inband Management IP
    # Tenants > mgmt > Node Management Addresses > Static Node Management Addresses
    resrc_desc = 'inb_mgmt_apic_{}'.format(name)
    class_name = 'mgmtRsInBStNode'
    tDn_string = "topology/pod-{}/node-{}".format(pod_id, node_id)
    dn_strings = "uni/tn-mgmt/mgmtp-default/inb-inb_epg/rsinBStNode-[topology/pod-{}/node-{}]".format(pod_id, node_id)
    path_attrs = '"/api/node/mo/uni/tn-mgmt.json"'

    # Format Variables for JSON Output
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

        # Define Variables for Template Creation - APIC Port Group to Interface Selector
        # Fabric > Access Policies > Interfaces > Leaf Interfaces > Profiles > {Leaf Profile Name} > {Port Selector}: Interface Policy Group
        resrc_desc = '{}_port_2_{}'.format(name, port_list_count)
        class_name = 'infraRsAccBaseGrp'
        tDn_string = "uni/infra/funcprof/accportgrp-inband_ap"
        path_attrs = '"/api/node/mo/uni/infra/accportprof-{}_IntProf/hports-Eth{}-{}-typ-range/rsaccBaseGrp.json"'.format(leaf, module, port)

        # Format Variables for JSON Output
        base_atts = {'tDn': tDn_string}
        data_out = {class_name: {'attributes': base_atts, 'children': []}}

        # Write Output to Resource Files using Template
        template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

    # Close the File created for this resource
    wr_file.close()

def resource_bgp_as(bgp_as):
    try:
        # Validate BGP AS Number
        validating.bgp_as(line_count, bgp_as)
    except Exception as err:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}.  Please verify Input Information.  Exiting....')
        print(f'\n-----------------------------------------------------------------------------\n')
        exit()
        
    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation - BGP Autonomous System Number
    # System > System Settings > BGP Route Reflector
    resrc_desc = 'bgp_as_{}'.format(bgp_as)
    class_name = "bgpAsP"
    rn_strings = "as"
    dn_strings = "uni/fabric/bgpInstP-default/{}".format(rn_strings)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)

    # Format Variables for JSON Output
    base_atts = {'dn': dn_strings, 'asn': bgp_as, 'rn': rn_strings}
    data_out = {class_name: {'attributes': base_atts, 'children': []}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)
    
def resource_bgp_rr(node_id):
    try:
        # Validate Node ID
        validating.node_id(line_count, node_id)
    except Exception as err:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}.  Please verify Input Information.  Exiting....')
        print(f'\n-----------------------------------------------------------------------------\n')
        exit()
        
    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation - BGP Route Reflectors
    # System > System Settings > BGP Route Reflector
    resrc_desc = 'bgp_rr_{}'.format(node_id)
    class_name = 'bgpRRNodePEp'
    rn_strings = "node-{}".format(node_id)
    dn_strings = "uni/fabric/bgpInstP-default/rr/node-{}".format(node_id)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)

    # Format Variables for JSON Output
    base_atts = {'dn': dn_strings, 'id': node_id, 'rn': rn_strings}
    data_out = {class_name: {'attributes': base_atts, 'children': []}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

def resource_dns(dns_ipv4, prefer):
    try:
        # Validate DNS IPv4 Address
        validating.ipv4(line_count, dns_ipv4)
    except Exception as err:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}.  Please verify Input Information.  Exiting....')
        print(f'\n-----------------------------------------------------------------------------\n')
        exit()
    
    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation - DNS Providers
    # Fabric > Fabric Policies > Policies > Global > DNS Profiles > default
    dns_ipv4_ = dns_ipv4.replace('.', '_')
    resrc_desc = 'dns_{}'.format(dns_ipv4_)
    class_name = 'dnsProv'
    rn_strings = "prov-[{}]".format(dns_ipv4)
    dn_strings = "uni/fabric/dnsp-default/{}".format(rn_strings)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)

    # Format Variables for JSON Output
    base_atts = {'dn': dn_strings, 'addr': dns_ipv4, 'preferred': prefer, 'rn': rn_strings}
    data_out = {class_name: {'attributes': base_atts, 'children': []}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

def resource_dns_mgmt(mgmt_domain):
    try:
        # Validate Management Domain
        mgmt_epg = validating.mgmt_domain(line_count, mgmt_domain)
    except Exception as err:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}.  Please verify Input Information.  Exiting....')
        print(f'\n-----------------------------------------------------------------------------\n')
        exit()
        
    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation - DNM Management Domain
    # Fabric > Fabric Policies > Policies > Global > DNS Profiles > default
    resrc_desc = 'dns_epg_{}'.format(mgmt_epg)
    class_name = 'dnsRsProfileToEpg'
    tDn_string = "uni/tn-mgmt/mgmtp-default/{}".format(mgmt_epg)
    path_attrs = '"/api/node/mo/uni/fabric/dnsp-default.json"'

    # Format Variables for JSON Output
    base_atts = {'tDn': tDn_string}
    data_out = {class_name: {'attributes': base_atts, 'children': []}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

def resource_domain(domain, prefer):
    try:
        # Validate Domain
        validating.domain(line_count, domain)
    except Exception as err:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}.  Please verify Input Information.  Exiting....')
        print(f'\n-----------------------------------------------------------------------------\n')
        exit()

    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation - Domains
    # Fabric > Fabric Policies > Policies > Global > DNS Profiles > default
    domain_ = domain.replace('.', '_')
    resrc_desc = 'domain_{}'.format(domain_)
    class_name = 'dnsDomain'
    rn_strings = "dom-[{}]".format(domain)
    dn_strings = "uni/fabric/dnsp-default/{}".format(rn_strings)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)

    # Format Variables for JSON Output
    base_atts = {'dn': dn_strings, 'name': domain, 'isDefault': prefer, 'rn': rn_strings}
    data_out = {class_name: {'attributes': base_atts, 'children': []}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

def resource_inband(inb_ipv4, inb_gwv4, inb_vlan):
    try:
        # Validate Inband VLAN
        validating.inb_vlan(line_count, inb_vlan)
    except Exception as err:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}.  Please verify Input Information.  Exiting....')
        print(f'\n-----------------------------------------------------------------------------\n')
        exit()

    # Which File to Write Data to
    file_inb = ('resources_user_import_Tenant_Mgmt.tf')
    wr_file = open(file_inb, 'w')
    wr_file.write('# Use this Resource File to Register the inband management network for the Fabric\n\n')

    
    # Define Variables for Template Creation - Inband VLAN Interface
    # Tenants > mgmt > Networking > Bridge Domains > inb: Policy > L3 Configurations > Subnets
    gwy_prefix = inb_ipv4.split('/', 2)
    gateway_v4 = str(inb_gwv4) + '/' + str(gwy_prefix[1])
    resrc_type = 'aci_subnet'
    resrc_desc = 'inb_subnet'
    attr_1st = 'parent_dn\t= aci_bridge_domain.inb.id'
    attr_2nd = 'ip\t\t\t= "{}"'.format(gateway_v4)
    attr_3rd = 'scope\t\t= ["public"]'

    # Write Output to Resource Files using Template
    template_aci_terraform_attr3(resrc_type, resrc_desc, attr_1st, attr_2nd, attr_3rd, wr_file)

    # Define Variables for Template Creation - Inband VLAN Pool
    # Fabric > Access Policies > Pools > VLAN > inband_vl-pool: Encap Blocks
    resrc_type = 'aci_ranges'
    resrc_desc = 'inb_vlan'
    attr_1st = 'vlan_pool_dn	= "uni/infra/vlanns-[inband_vl-pool]-static"'
    attr_2nd = '_from		    = "vlan-{}"'.format(inb_vlan)
    attr_3rd = 'to		        = "vlan-{}"'.format(inb_vlan)

    # Write Output to Resource Files using Template
    template_aci_terraform_attr3(resrc_type, resrc_desc, attr_1st, attr_2nd, attr_3rd, wr_file)

    # Define Variables for Template Creation - Inband Mgmt Default
    # Tenants > mgmt > Node Management EPGs > In-Band EPG
    resrc_desc = 'inb_mgmt_default_epg'
    class_name = 'mgmtInB'
    dn_strings = 'uni/tn-mgmt/mgmtp-default/inb-inb_epg'
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)
    descrption = 'Default Inband Mmgmt EPG Used by Brahma Startup Wizard.'
    encapsulat = 'vlan-{}'.format(inb_vlan)
    childclass = 'mgmtRsMgmtBD'
    child_Brdg = 'inb'

    # Format Variables for JSON Output
    base_atts = {'dn': dn_strings, 'descr': descrption, 'encap': encapsulat, 'name': 'inb_epg'}
    child_atts = {'tnFvBDName': child_Brdg}
    data_out = {class_name: {'attributes': base_atts, 'children': [{childclass: {'attributes': child_atts}}]}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

    # Close the File created for this resource
    wr_file.close()

def resource_ntp(ntp_ipv4, prefer, mgmt_domain):
    try:
        # Validate NTP IPv4 Address and Management Domain
        validating.ipv4(line_count, ntp_ipv4)
        mgmt_epg = validating.mgmt_domain(line_count, mgmt_domain)
    except Exception as err:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}.  Please verify Input Information.  Exiting....')
        print(f'\n-----------------------------------------------------------------------------\n')
        exit()

    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation - NTP Server
    # Fabric > Fabric Policies > Policies > Pod > Data and Time > Policy default
    ntp_ipv4_ = ntp_ipv4.replace('.', '_')
    resrc_desc = 'ntp_{}'.format(ntp_ipv4_)
    class_name = 'datetimeNtpProv'
    rn_strings = 'ntpprov-{}'.format(ntp_ipv4)
    dn_strings = 'uni/fabric/time-default/{}'.format(rn_strings)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)
    childclass = 'datetimeRsNtpProvToEpg'
    child_tDn = 'uni/tn-mgmt/mgmtp-default/{}'.format(mgmt_epg)

    # Format Variables for JSON Output
    base_atts = {'dn': dn_strings, 'name': ntp_ipv4, 'preferred': prefer, 'rn': rn_strings}
    child_atts = {childclass: {'attributes': {'tDn': child_tDn}}}
    child_combined = [child_atts]
    data_out = {class_name: {'attributes': base_atts, 'children': child_combined}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

def resource_SmarthCallHome(smtp_port, smtp_relay, mgmt_domain, ch_fr_email, ch_rp_email, ch_to_email, phone_numbr, contact_inf,
                            str_address, contract_id, customer_id, site_identi):
    try:
        # Validate All the Email Addresses, Phone Number, and Management Domain
        validating.email(line_count, ch_fr_email)
        validating.email(line_count, ch_rp_email)
        validating.email(line_count, ch_to_email)
        validating.phone(line_count, phone_numbr)
        mgmt_epg = validating.mgmt_domain(line_count, mgmt_domain)
    except Exception as err:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}.  Please verify Input Information.  Exiting....\n')
        print(f'\n-----------------------------------------------------------------------------\n')
        exit()

    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation - SmartCallHome Destination Group
    # Admin > External Data Collectors >  Monitoring Destinations > Smart callhome
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

    # Format Variables for JSON Output
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

    # Define Variables for Template Creation - Smart Callhome Source
    # Fabric > Fabric Policies > Policies > Monitoring >  Common Policy > Callhome/Smart Callhome/SNMP/Syslog/TACACS > Smart Callhome
    resrc_desc = 'callhomeSmartSrc'
    class_name = 'callhomeSmartSrc'
    rn_strings = "smartchsrc"
    dn_strings = "uni/infra/moninfra-default/{}".format(rn_strings)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)
    name = 'SmartCallHome_dg'
    child_1_class = 'callhomeRsSmartdestGroup'
    child_1_tDn = 'uni/fabric/smartgroup-SmartCallHome_dg'

    # Format Variables for JSON Output
    base_atts = {'dn': dn_strings, 'rn': rn_strings}
    child_1_atts = {child_1_class: {'attributes': {'tDn': child_1_tDn}, 'children': []}}
    child_combined = [child_1_atts]
    data_out = {class_name: {'attributes': base_atts, 'children': child_combined}}
    
    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

def resource_snmp_client(client_name, client_ipv4, mgmt_domain):
    try:
        # Validate SNMP IPv4 Client Address and Management Domain
        validating.ipv4(line_count, client_ipv4)
        snmp_mgmt = validating.snmp_mgmt(line_count, mgmt_domain)
    except Exception as err:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}.  Please verify Input Information.  Exiting....')
        print(f'\n-----------------------------------------------------------------------------\n')
        exit()

    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation
    # Fabric > Fabric Policies > Policies > Pod >  SNMP > default
    client_ipv4_ = client_ipv4.replace('.', '_')
    resrc_desc = 'snmp_client_{}'.format(client_ipv4_)
    class_name = 'snmpClientP'
    rn_strings = "client-{}".format(client_ipv4)
    dn_strings = "uni/fabric/snmppol-default/clgrp-{}_Clients/client-[{}]".format(snmp_mgmt, client_ipv4)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)

    # Format Variables for JSON Output
    base_atts = {'dn': dn_strings, 'name': client_name, 'addr': client_ipv4, 'rn': rn_strings}
    data_out = {class_name: {'attributes': base_atts, 'children': []}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

def resource_snmp_comm(community, description):
    try:
        # Validate SNMP Community
        validating.snmp_string(line_count, community)
    except Exception as err:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}.  Please verify Input Information.  Exiting....\n')
        print(f'\n-----------------------------------------------------------------------------\n')
        exit()

    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation - SNMP Communities
    # Fabric > Fabric Policies > Policies > Pod >  SNMP > default
    resrc_desc = 'snmp_comm_{}'.format(community)
    class_name = 'snmpCommunityP'
    rn_strings = "community-{}".format(community)
    dn_strings = "uni/fabric/snmppol-default/{}".format(rn_strings)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)

    # Format Variables for JSON Output
    base_atts = {'dn': dn_strings, 'descr': description, 'name': community, 'rn': rn_strings}
    data_out = {class_name: {'attributes': base_atts, 'children': []}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

    wr_comm.write('%s\n' % (community))

def resource_snmp_info(contact, location):
    try:
        # Validate SNMP Information STrings
        validating.snmp_info(line_count, contact, location)
    except Exception as err:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}.  Please verify Input Information.  Exiting....\n')
        print(f'\n-----------------------------------------------------------------------------\n')
        exit()

    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation
    # Fabric > Fabric Policies > Policies > Pod >  SNMP > default
    resrc_desc = 'snmp_info'
    class_name = 'snmpPol'
    dn_strings = "uni/fabric/snmppol-default"
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)
    descrption = 'This is the default SNMP Policy'

    # Format Variables for JSON Output
    base_atts = {'dn': dn_strings, 'descr': descrption, 'adminSt': 'enabled', 'contact': contact, 'loc': location}
    data_out = {class_name: {'attributes': base_atts, 'children': []}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

def resource_snmp_trap(snmp_ipv4, snmp_port, snmp_vers, snmp_string, snmp_auth, mgmt_domain):
    
    try:
        # Validate SNMP Trap Server IPv4 Address, SNMP Port, Check SNMP Version
        # Check SNMP Community/Username and Validate Management Domain
        validating.ipv4(line_count, snmp_ipv4)
        validating.port(line_count, snmp_port)
        validating.snmp_ver(line_count, snmp_vers)
        validating.snmp_string(line_count, snmp_string)
        mgmt_epg = validating.mgmt_domain(line_count, mgmt_domain)
    except Exception as err:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}.  Please verify Input Information.  Exiting....')
        print(f'\n-----------------------------------------------------------------------------\n')
        exit()

    # Set noauth if v1 or v2c
    if re.search('(v1|v2c)', snmp_vers):
        snmp_auth = 'noauth'
    
    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation
    # Fabric > Fabric Policies > Policies > Pod >  SNMP > default
    snmp_ipv4_ = snmp_ipv4.replace('.', '_')
    resrc_desc = 'snmp_trap_default_{}'.format(snmp_ipv4_)
    class_name = 'snmpTrapFwdServerP'
    dn_strings = "uni/fabric/snmppol-default/trapfwdserver-[{}]".format(snmp_ipv4)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)

    # Format Variables for JSON Output
    if snmp_port == '':
        base_atts = {'dn': dn_strings, 'addr': snmp_ipv4,}
    else:
        base_atts = {'dn': dn_strings, 'addr': snmp_ipv4, 'port': snmp_port}
    data_out = {class_name: {'attributes': base_atts, 'children': []}}
    
    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)
    
    # Define Variables for Template Creation - SNMP Trap Destination Group
    # Admin > External Data Collectors >  Monitoring Destinations > SNMP
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
    
    # Format Variables for JSON Output
    base_atts = {'dn': dn_strings, 'descr': descrption, 'name': name, 'rn': rn_strings}
    sub_child = {sub_child_class: {'attributes': {'tDn': sub_child_tDn}}}
    child_atts = {childclass: {'attributes': {'dn': child_Dn, 'ver': snmp_vers, 'host': snmp_ipv4, 'port': snmp_port,
                  'secName': snmp_string, 'v3SecLvl': snmp_auth, 'rn': child_Rn}, 'children': [sub_child]}}
    child_combined = [child_atts]
    data_out = {class_name: {'attributes': base_atts, 'children': child_combined}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

def resource_snmp_user(snmp_user, priv_type, priv_key, auth_type, auth_key):
    try:
        # Validate SNMP User Authentication Information
        validating.snmp_auth(line_count, auth_key, priv_key, priv_type)
    except Exception as err:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}.  Please verify Input Information.  Exiting....\n')
        print(f'\n-----------------------------------------------------------------------------\n')
        exit()

    # Modify User Input of priv_type or auth_type to send to APIC
    if priv_type == 'none':
        priv_type = ''
    if auth_type == 'md5':
        auth_type = ''
    if auth_type == 'sha1':
        auth_type = 'hmac-sha1-96'
    
    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation - SNMP User
    # Fabric > Fabric Policies > Policies > Pod >  SNMP > default
    resrc_desc = 'snmp_user_{}'.format(snmp_user)
    class_name = 'snmpUserP'
    dn_strings = "uni/fabric/snmppol-default/user-{}".format(snmp_user)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)

    # Format Variables for JSON Output
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
        # Validate Serial Number, Hostname, node_id, node_type, pod_id,
        # switch_role, modules, port_count, oob_ipv4, oob_gwv4, inb_ipv4,
        # inb_gwv4, inb_vlan
        validating.hostname(line_count, name)
        validating.node_id(line_count, node_id)
        validating.node_type(line_count, name, node_type)
        validating.pod_id(line_count, name, pod_id)
        validating.role(line_count, name, switch_role)
        validating.modules(line_count, name, switch_role, modules)
        validating.port_count(line_count, name, switch_role, port_count)
        validating.inband(line_count, name, inb_ipv4, inb_gwv4)
        validating.oob(line_count, name, oob_ipv4, oob_gwv4)
    except Exception as err:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}.  Please verify input information.  Exiting....')
        print(f'\n-----------------------------------------------------------------------------\n')
        exit()

    # Determine if Node is Odd or Even and Add to appropriate maintenance Group
    node_id = int(node_id)
    if node_id % 2 == 0:
        Maint_Grp = 'switch_MgB'
    else:
        Maint_Grp = 'switch_MgA'
    node_id = str(node_id)

    # Which File to Write Data to
    file_sw = 'resources_user_import_xDevice_{}.tf'.format(name)
    wr_file = open(file_sw, 'w')

    wr_file.write(f'# Use this Resource File to Register {name} with node id {node_id} to the Fabric\n')
    wr_file.write('# Requirements are:\n')
    wr_file.write('# serial: Actual Serial Number of the switch.\n')
    wr_file.write('# name: Hostname you want to assign.\n')
    wr_file.write('# node_id: unique ID used to identify the switch in the APIC.\n')
    wr_file.write('#   in the "Cisco ACI Object Naming and Numbering: Best Practice\n')
    wr_file.write('#   The recommendation is that the Spines should be 101-199\n')
    wr_file.write('#   and leafs should start at 200+ thru 4000.  As the number of\n')
    wr_file.write('#   spines should always be less than the number of leafs\n')
    wr_file.write('#   https://www.cisco.com/c/en/us/td/docs/switches/datacenter/aci/apic/sw/kb/b-Cisco-ACI-Naming-and-Numbering.html#id_107280\n')
    wr_file.write('# node_type: uremote-leaf-wan or unspecified.\n')
    wr_file.write('# role: spine, leaf.\n')
    wr_file.write('# pod_id: Typically this will be one unless you are running multipod.\n\n')

    # Create Switch Fabric Membership Record
    # Fabric > Inventory > Fabric Membership: Registered Nodes
    wr_file.write('resource "aci_fabric_node_member" "%s" {\n' % (name))
    wr_file.write('\tserial    = "%s"\n' % (serial))
    wr_file.write('\tname      = "%s"\n' % (name))
    wr_file.write('\tnode_id   = "%s"\n' % (node_id))
    wr_file.write('\tnode_type = "%s"\n' % (node_type))
    wr_file.write('\trole      = "%s"\n' % (switch_role))
    wr_file.write('\tpod_id    = "%s"\n' % (pod_id))
    wr_file.write('}\n')
    wr_file.write('\n')

    # Define Variables for Template Creation - OOB IPv4
    # Tenants > mgmt > Node Management Addresses > Static Node Management Addresses
    resrc_desc = 'oob_mgmt_{}'.format(name)
    class_name = 'mgmtRsOoBStNode'
    dn_strings = "uni/tn-mgmt/mgmtp-default/oob-default/rsooBStNode-[topology/pod-{}/node-{}]".format(pod_id, node_id)
    path_attrs = '"/api/node/mo/uni/tn-mgmt.json"'
    tDn_string = 'topology/pod-{}/node-{}'.format(pod_id, node_id)

    # Format Variables for JSON Output
    base_atts = {'dn': dn_strings, 'addr': oob_ipv4, 'gw': oob_gwv4, 'tDn': tDn_string, 'v6Addr': '::', 'v6Gw': '::'}
    data_out = {class_name: {'attributes': base_atts}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

    # Define Variables for Template Creation - Inband IPv4
    # Tenants > mgmt > Node Management Addresses > Static Node Management Addresses
    resrc_desc = 'inb_mgmt_{}'.format(name)
    class_name = 'mgmtRsInBStNode'
    dn_strings = "uni/tn-mgmt/mgmtp-default/inb-inb_epg/rsinBStNode-[topology/pod-{}/node-{}]".format(pod_id, node_id)
    path_attrs = '"/api/node/mo/uni/tn-mgmt.json"'
    tDn_string = 'topology/pod-{}/node-{}'.format(pod_id, node_id)

    # Format Variables for JSON Output
    base_atts = {'dn': dn_strings, 'addr': inb_ipv4, 'gw': inb_gwv4, 'tDn': tDn_string, 'v6Addr': '::', 'v6Gw': '::'}
    data_out = {class_name: {'attributes': base_atts}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

    # Define Variables for Template Creation - Maintenance Group
    # Admin > Firmware > Infrastructure > Nodes
    resrc_desc = 'maint_grp_{}'.format(name)
    class_name = 'maintMaintGrp'
    dn_strings = 'uni/fabric/maintgrp-{}'.format(Maint_Grp)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)
    childclass = 'fabricNodeBlk'
    child_name = 'blk{}-{}'.format(node_id, node_id)
    child_Rn = 'nodeblk-blk{}-{}'.format(node_id, node_id)
    child_Dn = 'uni/fabric/maintgrp-{}/{}'.format(Maint_Grp, child_Rn)

    # Format Variables for JSON Output
    base_atts = {'dn': dn_strings}
    child_atts = {childclass: {'attributes': {'dn': child_Dn, 'name': child_name, 'from_': node_id, 'to_': node_id, 'rn': child_Rn},}}
    child_combined = [child_atts]
    data_out = {class_name: {'attributes': base_atts, 'children': child_combined}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

    if switch_role == 'leaf':
        # Define Variables for Template Creation - ACI Leaf Profile
        # Fabric > Access Policies > Switches > Leaf Switches > Profiles
        wr_file.write('resource "aci_leaf_profile" "%s_SwSel" {\n' % (name))
        wr_file.write('\tname = "%s_SwSel"\n' % (name))
        wr_file.write('\tleaf_selector {\n')
        wr_file.write('\t\tname                    = "%s"\n' % (name))
        wr_file.write('\t\tswitch_association_type = "range"\n')
        wr_file.write('\t\tnode_block {\n')
        wr_file.write('\t\t\tname  = "%s"\n' % (name))
        wr_file.write('\t\t\tfrom_ = "%s"\n' % (node_id))
        wr_file.write('\t\t\tto_   = "%s"\n' % (node_id))
        wr_file.write('\t\t}\n')
        wr_file.write('\t}\n')
        wr_file.write('}\n')
        wr_file.write('\n')


        # Define Variables for Template Creation - Leaf Interface Profile
        # Fabric > Access Policies > Interfaces > Leaf interfaces > Profiles
        resrc_type = 'aci_leaf_interface_profile'
        resrc_desc = '{}_IntProf'.format(name)
        attr_1st = 'name	= "{}_IntProf"'.format(name)

        # Write Output to Resource Files using Template
        template_aci_terraform_attr1(resrc_type, resrc_desc, attr_1st, wr_file)

        # Define Variables for Template Creation - Leaf Port Selector to Switch Selector
        # Fabric > Access Policies > Switches > Leaf Switches > Profiles: {Leaf Profile}: Associated Interface Selector Profile
        resrc_desc = 'leaf_int_selector_{}_IntProf'.format(name)
        class_name = 'infraRsAccPortP'
        tDn_string = "uni/infra/accportprof-{}_IntProf".format(name)
        path_attrs = '"/api/node/mo/uni/infra/nprof-{}_SwSel.json"'.format(name)

        # Format Variables for JSON Output
        base_atts = {'tDn': tDn_string}
        data_out = {class_name: {'attributes': base_atts}}

        # Write Output to Resource Files using Template
        template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

        mod_count = 0
        while mod_count < int(modules):
            mod_count += 1
            # Define Variables for Template Creation - Leaf Port Selector Interface Selectors
            # Fabric > Access Policies > Interfaces > Leaf interfaces > Profiles {Leaf Profile}: Associated Interface Selectors
            wr_file.write('resource "aci_rest" "%s_%s_IntProf" {\n' % (name, mod_count))
            wr_file.write('\tfor_each         = var.port-selector-%s\n' %(port_count))
            wr_file.write('\tpath             = "/api/node/mo/uni/infra/accportprof-%s_IntProf/hports-Eth%s-${each.value.name}-typ-range.json"\n' % (name, mod_count))
            wr_file.write('\tclass_name       = "infraHPortS"\n')
            wr_file.write('\tpayload          = <<EOF\n')

            class_name = 'infraHPortS'
            rn_strings = 'hports-Eth%s-${each.value.name}-typ-range' % (mod_count)
            dn_strings = 'uni/infra/accportprof-%s_IntProf/%s' % (name, rn_strings)
            name_port = 'Eth%s-${each.value.name}' % (mod_count)
            childclass = 'infraPortBlk'
            child_name = 'block2'
            child_port = '${each.value.name}'
            child_Rn = 'portblk-block2'
            child_Dn = 'uni/infra/accportprof-%s_IntProf/hports-Eth%s-${each.value.name}-typ-range/%s' % (name, mod_count, child_Rn)
            mod_num = '%s' % (mod_count)

            # Format Variables for JSON Output
            base_atts = {'dn': dn_strings, 'name': name_port, 'rn': rn_strings}
            child_atts = {childclass: {'attributes': {'dn': child_Dn, 'fromCard': mod_num, 'fromPort': child_port, 'toCard': mod_num,
                          'toPort': child_port, 'name': child_name, 'rn': child_Rn},}}
            child_combined = [child_atts]
            data_out = {class_name: {'attributes': base_atts, 'children': child_combined}}

            # Write Output to Resource File
            wr_file.write(json.dumps(data_out, indent=4))

            wr_file.write('\n\tEOF\n')
            wr_file.write('}\n')
            wr_file.write('\n')
    elif switch_role == 'spine':
        # Define Variables for Template Creation - ACI Spine Profile
        # Fabric > Access Policies > Switches > Spine Switches > Profiles
        resrc_type = 'aci_spine_profile'
        resrc_desc = '{}_SwSel'.format(name)
        attr_1st = 'name = "{}_SwSel"'.format(name)

        # Write Output to Resource Files using Template
        template_aci_terraform_attr1(resrc_type, resrc_desc, attr_1st, wr_file)

        # Define Variables for Template Creation - Spine Interface Profile
        # Fabric > Access Policies > Interfaces > Spine interfaces > Profiles
        resrc_type = 'aci_spine_interface_profile'
        resrc_desc = '{}_IntProf'.format(name)
        attr_1st = 'name = "{}_IntProf"'.format(name)

        # Write Output to Resource Files using Template
        template_aci_terraform_attr1(resrc_type, resrc_desc, attr_1st, wr_file)

        # Define Variables for Template Creation - Spine Selectors to Switch Selector
        # Fabric > Access Policies > Switches > Spine Switches > Profiles: {Spine Profile}: Spine Selectors
        resrc_type = 'aci_spine_switch_association'
        resrc_desc = '{}'.format(name)
        attr_1st = 'spine_profile_dn              = aci_spine_profile.{}_SwSel.id'.format(name)
        attr_2st = 'name                          = "{}"'.format(name)
        attr_3st = 'spine_switch_association_type = "range"'

        # Write Output to Resource Files using Template
        template_aci_terraform_attr3(resrc_type, resrc_desc, attr_1st, attr_2st, attr_3st, wr_file)

        # Define Variables for Template Creation - Spine Port Selector to Switch Selector
        # Fabric > Access Policies > Switches > Spine Switches > Profiles: {Spine Profile}: Associated Interface Selector Profile
        resrc_type = 'aci_spine_port_selector'
        resrc_desc = '{}'.format(name)
        attr_1st = 'spine_profile_dn              = aci_spine_profile.{}_SwSel.id'.format(name)
        attr_2st = 'tdn                           = aci_spine_interface_profile.{}_IntProf.id'.format(name)

        # Write Output to Resource Files using Template
        template_aci_terraform_attr2(resrc_type, resrc_desc, attr_1st, attr_2st, wr_file)

        mod_count = 0
        while mod_count < int(modules):
            # Define Variables for Template Creation - Spine Port Selector Interface Selectors
            # Fabric > Access Policies > Interfaces > Spine interfaces > Profiles {Spine Profile}: Associated Interface Selectors
            mod_count += 1
            wr_file.write('resource "aci_rest" "%s_%s_IntProf" {\n' % (name, mod_count))
            wr_file.write('\tfor_each         = var.port-selector-%s\n' %(port_count))
            wr_file.write('\tpath             = "/api/node/mo/uni/infra/spaccportprof-%s_IntProf/shports-Eth%s-${each.value.name}-typ-range.json"\n' % (name, mod_count))
            wr_file.write('\tclass_name       = "infraSHPortS"\n')
            wr_file.write('\tpayload          = <<EOF\n')

            class_name = 'infraSHPortS'
            rn_strings = 'shports-Eth%s-${each.value.name}-typ-range' % (mod_count)
            dn_strings = 'uni/infra/spaccportprof-%s_IntProf/%s' % (name, rn_strings)
            name_port = 'Eth%s-${each.value.name}' % (mod_count)
            childclass = 'infraPortBlk'
            child_name = 'block2'
            child_port = '${each.value.name}'
            child_Rn = 'portblk-block2'
            child_Dn = 'uni/infra/spaccportprof-%s_IntProf/shports-Eth%s-${each.value.name}-typ-range/%s' % (name, mod_count, child_Rn)
            mod_num = '%s' % (mod_count)

            # Format Variables for JSON Output
            base_atts = {'dn': dn_strings, 'name': name_port, 'rn': rn_strings}
            child_atts = {childclass: {'attributes': {'dn': child_Dn, 'fromCard': mod_num, 'fromPort': child_port, 'toCard': mod_num,
                          'toPort': child_port, 'name': child_name, 'rn': child_Rn},}}
            child_combined = [child_atts]
            data_out = {class_name: {'attributes': base_atts, 'children': child_combined}}

            # Write Output to Resource File
            wr_file.write(json.dumps(data_out, indent=4))

            wr_file.write('\n\tEOF\n')
            wr_file.write('}\n')
            wr_file.write('\n')
    wr_file.close()

def resource_syslog(syslog_ipv4, syslog_port, mgmt_domain, severity, facility, local_state, local_level, console_state, console_level):
    try:
        # Validate Syslog Server IPv4 Address, Port, Facility, Logging Levels and Management Domain
        validating.ipv4(line_count, syslog_ipv4)
        validating.port(line_count, syslog_port)
        validating.syslog_fac(line_count, facility)
        validating.log_level(line_count, 'remote', severity)
        validating.log_level(line_count, 'local', local_level)
        validating.log_level(line_count, 'console', console_level)
        mgmt_epg = validating.mgmt_domain(line_count, mgmt_domain)
    except Exception as err:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}.  Please verify Input Information.  Exiting....')
        print(f'\n-----------------------------------------------------------------------------\n')
        exit()

    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation - Syslog
    # Admin > External Data Collectors >  Monitoring Destinations > Syslog
    # Fabric > Fabric Policies > Policies > Monitoring >  Common Policy > Callhome/Smart Callhome/SNMP/Syslog/TACACS > Sylsog
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
    
    # Format Variables for JSON Output
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

def resource_tacacs(login_domain, tacacs_ipv4, tacacs_port, tacacs_key, auth_proto, tac_timeout, tac_retry, mgmt_domain, tacacs_order_count):
    try:
        # Validate TACACS IPv4 Address, Login Domain, Authentication Protocol,
        # secret, Timeout, Retry Limit and Management Domain
        validating.login_domain(line_count, login_domain)
        validating.auth_proto(line_count, auth_proto)  
        validating.tacacs_key(line_count, tacacs_key)
        validating.tac_timeout(line_count, tac_timeout)
        validating.tac_retry(line_count, tac_retry)
        validating.ipv4(line_count, tacacs_ipv4)
        mgmt_epg = validating.mgmt_domain(line_count, mgmt_domain)
    except Exception as err:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}.  Please verify Input Information.  Exiting....\n')
        print(f'\n-----------------------------------------------------------------------------\n')
        exit()

    # Which File to Write Data to
    wr_file = wr_base_info

    # Define Variables for Template Creation - TACACS+ Accounting Destination Group
    # Admin > External Data Collectors >  Monitoring Destinations > TACACS
    group_name = 'TACACS_acct'
    tacacs_ipv4_ = tacacs_ipv4.replace('.', '_')
    resrc_desc = 'tacacs_{}_{}'.format(group_name, tacacs_ipv4_)
    class_name = 'tacacsGroup'
    rn_strings = 'tacacsgroup-{}'.format(group_name)
    dn_strings = 'uni/fabric/{}'.format(rn_strings)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)
    descrption = 'TACACS Accounting Group {} - Created by Brahma Startup Wizard'.format(group_name)
    childclass = 'tacacsTacacsDest'
    child_Rn = 'tacacsdest-{}-port-{}'.format(tacacs_ipv4, tacacs_port)
    child_Dn = 'uni/fabric/tacacsgroup-{}/{}'.format(group_name, child_Rn)
    sub_child_class = 'fileRsARemoteHostToEpg'
    sub_child_tDn = 'uni/tn-mgmt/mgmtp-default/{}'.format(mgmt_epg)

    # Format Variables for JSON Output
    base_atts = {'dn': dn_strings, 'descr': descrption, 'name': group_name, 'rn': rn_strings}
    sub_child = {sub_child_class: {'attributes': {'tDn': sub_child_tDn}}}
    child_atts = {childclass: {'attributes': {'dn': child_Dn, 'authProtocol': auth_proto, 'host': tacacs_ipv4, 'key': tacacs_key,
                  'rn': child_Rn}, 'children': [sub_child]}}
    child_combined = [child_atts]
    data_out = {class_name: {'attributes': base_atts, 'children': child_combined}}

    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

    if tacacs_order_count == 1:
        # Define Variables for Template Creation - TACACS Source
        # Fabric > Fabric Policies > Policies > Monitoring >  Common Policy > Callhome/Smart Callhome/SNMP/Syslog/TACACS > TACACS
        resrc_desc = 'tacacsSrc'
        class_name = 'tacacsSrc'
        rn_strings = "tacacssrc-TACACS_Src"
        dn_strings = "uni/fabric/moncommon/{}".format(rn_strings)
        path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)
        name_src = 'TACACS_Src'
        child_1_class = 'tacacsRsDestGroup'
        child_1_tDn = 'uni/fabric/tacacsgroup-{}'.format(group_name)

        # Format Variables for JSON Output
        base_atts = {'dn': dn_strings, 'name': name_src, 'rn': rn_strings}
        child_1_atts = {child_1_class: {'attributes': {'tDn': child_1_tDn}, 'children': []}}
        child_combined = [child_1_atts]
        data_out = {class_name: {'attributes': base_atts, 'children': child_combined}}
        
        # Write Output to Resource Files using Template
        template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

    # Define Variables for Template Creation - TACACS+ Provider
    # Admin > AAA > Authentication: TACACS
    resrc_desc = 'aaaTacacsPlusProvider_{}'.format(tacacs_ipv4_)
    class_name = 'aaaTacacsPlusProvider'
    rn_strings = "tacacsplusprovider-{}".format(tacacs_ipv4)
    dn_strings = "uni/userext/tacacsext/{}".format(rn_strings)
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)
    descrption = 'TACACS+ Provider - {}.  Added by Brahma Startup Wizard.'.format(tacacs_ipv4)
    child_1_class = 'aaaRsSecProvToEpg'
    child_1_tDn = 'uni/tn-mgmt/mgmtp-default/{}'.format(mgmt_epg)

    # Format Variables for JSON Output
    base_atts = {'dn': dn_strings, 'timeout': tac_timeout, 'retries': tac_retry, 'monitorServer': 'disabled', 'key': tacacs_key, 
                 'authProtocol': auth_proto, 'name': tacacs_ipv4, 'descr': descrption, 'rn': rn_strings}
    child_1_atts = {child_1_class: {'attributes': {'tDn': child_1_tDn}, 'children': []}}
    child_combined = [child_1_atts]
    data_out = {class_name: {'attributes': base_atts, 'children': child_combined}}
    
    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

    # Define Variables for Template Creation - External Login Domain - TACACS+
    # Admin > AAA > Authentication: AAA > Login Domains
    provider_group = 'TACACS'
    resrc_desc = 'Ext_Login_TACACS_prov-{}'.format(tacacs_ipv4_)
    class_name = 'aaaUserEp'
    dn_strings = "uni/userext"
    path_attrs = '"/api/node/mo/{}.json"'.format(dn_strings)
    child_1_class = 'aaaLoginDomain'
    child_1_Rn = 'logindomain-{}'.format(login_domain)
    child_1_Dn = 'uni/userext/{}'.format(child_1_Rn)
    sub_child_1_class = 'aaaDomainAuth'
    sub_child_1_Rn = 'domainauth'
    sub_child_1_Dn = 'uni/userext/logindomain-{}/domainauth'.format(login_domain)
    sub_child_1_desc = 'TACACS+ Login Domain {}. Created by Brahma Wizard.'.format(login_domain)
    child_2_class = 'aaaTacacsPlusEp'
    child_2_Dn = 'uni/userext/tacacsext'
    sub_child_2_class = 'aaaTacacsPlusProviderGroup'
    sub_child_2_Dn = 'uni/userext/tacacsext/tacacsplusprovidergroup-{}'.format(provider_group)
    basement_2_class = 'aaaProviderRef'
    basement_2_dn = 'uni/userext/tacacsext/tacacsplusprovidergroup-{}/providerref-{}'.format(provider_group, tacacs_ipv4)
    print(f'count is {tacacs_order_count}')
    basement_order = '{}'.format(tacacs_order_count)
    basement_descr = 'Added TACACS Server {} - Brahma Startup Wizard'.format(tacacs_ipv4)

    # Format Variables for JSON Output
    base_atts = {'dn': dn_strings}
    sub_1_atts = {sub_child_1_class: {'attributes': {'dn': sub_child_1_Dn, 'providerGroup': provider_group, 'realm': 'tacacs',
                  'descr': sub_child_1_desc, 'rn': sub_child_1_Rn}, 'children': []}}
    child_1_atts = {child_1_class: {'attributes': {'dn': child_1_Dn, 'name': login_domain, 'rn': child_1_Rn}, 'children': [sub_1_atts]}}
    basement_2_atts = {basement_2_class: {'attributes': {'dn': basement_2_dn, 'order': basement_order, 'name': tacacs_ipv4,
                       'descr': basement_descr}, 'children': []}}
    sub_2_atts = {sub_child_2_class: {'attributes': {'dn': sub_child_2_Dn}, 'children': [basement_2_atts]}}
    child_2_atts = {child_2_class: {'attributes': {'dn': child_2_Dn}, 'children': [sub_2_atts]}}

    child_combined = [child_1_atts, child_2_atts]
    data_out = {class_name: {'attributes': base_atts, 'children': child_combined}}
    
    # Write Output to Resource Files using Template
    template_aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

with open(csv_input) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    count_inb_gwv4 = 0
    count_inb_vlan = 0
    count_dns_servers = 0
    tacacs_order_count = 0
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
                validating.inb_vlan_exist(inb_vlan)

                # Create Resource Record for Switch and inband Bridge  Domain AP/EPG
                resource_apic_inb(name, node_id, pod_id, inb_ipv4, inb_gwv4, inb_vlan, p1_leaf, p1_swpt, p2_leaf, p2_swpt)
                if count_inb_gwv4 == 0: 
                    resource_inband(inb_ipv4, inb_gwv4, inb_vlan)
                    count_inb_gwv4 += 1
                    current_inb_gwv4 = inb_gwv4
                else:
                    validating.match_current_gw(line_count, current_inb_gwv4, inb_gwv4)
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
                    print(f'\n-----------------------------------------------------------------------------\n')
                    print(f'   At this time it is only supported to add two DNS Providers')
                    print(f'   Remove one or more providers.  Exiting....\n')
                    print(f'\n-----------------------------------------------------------------------------\n')
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
                validating.inb_vlan_exist(inb_vlan)

                # Create Resource Record for Switch and inband Bridge  Domain AP/EPG
                resource_switch(serial, name, node_id, node_type, pod_id, switch_role, modules, port_count, oob_ipv4, oob_gwv4, 
                                inb_ipv4, inb_gwv4, inb_vlan)
                if count_inb_gwv4 == 0: 
                    resource_inband(inb_ipv4, inb_gwv4, inb_vlan)
                    count_inb_gwv4 += 1
                    current_inb_gwv4 = inb_gwv4
                else:
                    validating.match_current_gw(line_count, current_inb_gwv4, inb_gwv4)
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
            elif type == 'tacacs':
                login_domain = column[1]
                tacacs_ipv4 = column[2]
                tacacs_port = column[3]
                tacacs_key = column[4]
                auth_proto = column[5]
                tac_timeout = column[6]
                tac_retry  = column[7]
                mgmt_domain = column[8]
                tacacs_order_count += 1
                # Build TACACS+ Configuration
                resource_tacacs(login_domain, tacacs_ipv4, tacacs_port, tacacs_key, auth_proto, tac_timeout, tac_retry, mgmt_domain, tacacs_order_count)
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
print(f'\n-----------------------------------------------------------------------------\n')
print(f'   Completed Running Script.  Existing....')
print(f'\n-----------------------------------------------------------------------------\n')
exit()