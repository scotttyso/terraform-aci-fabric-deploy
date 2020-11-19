#!/usr/bin/env python3

import validators
import json
import testvalidator

template_m = '{0} {1}\n\tpath\t\t= {2}\n\tclass_name\t= {3}\n\tpayload\t\t= <<EOF\n{4}\n\tEOF\n{5}\n\n'
append = ""
cvs_input = ""


def resource_apic_inb(name, node_id, pod_id, inb_ipv4, inb_gwv4, inb_vlan, p1_leaf, p1_swpt, p2_leaf, p2_swpt, line_count):
    try:
        # Validate APIC Node_ID
        testvalidator.validate_node_id_apic(line_count, name, node_id)

        # Validate Pod_ID
        testvalidator.validate_pod_id(line_count, name, pod_id)

        # Validate InBand Network
        testvalidator.validate_inband(line_count, name, inb_ipv4, inb_gwv4)
    except Exception as err:
        print('\r\r----------------\r')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}, Please verify input information.')
        print('----------------\r\r')
        exit()

    # PART A
    pod_id = str(pod_id)
    resource_a = 'resource "aci_rest" "inb_mgmt_apic_{}"'.format(name)
    class_name_a = '"mgmtRsInBStNode"'
    path_a = '"/api/node/mo/uni/tn-mgmt.json"'
    dn_aa = "uni/tn-mgmt/mgmtp-default/inb-inb_epg/rsinBStNode-[topology/pod-{}/node-{}]".format(pod_id, node_id)
    tDn_aa = "topology/pod-{}/node-{}".format(pod_id, node_id)

    level3a = {'addr': inb_ipv4, 'dn': dn_aa, 'gw': inb_gwv4, 'tDn': tDn_aa}
    level2a = {"attributes": level3a}
    level1a = {"mgmtRsInBStNode": level2a}
    data_a = level1a

    # Create template for writing file
    temp_a = template_m.format(resource_a, "{", path_a, class_name_a, json.dumps(data_a, indent=4), "}")

    file_apic = ('resources_user_import_xDevice_%s.tf' % (name))
    with open(file_apic, 'w') as f:
        f.write(temp_a)

    # PART B (Possibly make this a separate function?)
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

        resource_b = 'resource "aci_rest" "{}_port_2_{}"'.format(name, port_list_count)
        path_b = '"/api/node/mo/uni/infra/accportprof-{}_IntProf/hports-Eth{}-{}-typ-range/rsaccBaseGrp.json"'.format(leaf, module, port)
        class_name_b = '"infraRsAccBaseGrp"'
        tDn_bb = "uni/infra/funcprof/accportgrp-inband_ap"

        level3b = {'tDn': tDn_bb}
        level2b = {'attributes': level3b}
        level1b = {"infraRsAccBaseGrp": level2b}
        data_b = level1b

        temp_b = template_m.format(resource_b, "{", path_b, class_name_b, json.dumps(data_b, indent=4), "}")

        with open(file_apic, 'a') as f:
            f.write(temp_b)


def resource_bgp_as(bgp_as, line_count, wr_base_info):
    # Validate BGP AS Number
    testvalidator.validate_bgp_as(line_count, bgp_as)

    resource_a = 'resource "aci_rest" "bgp_as"'
    path_a = '"/api/node/mo/uni/fabric/bgpInstP-default/as.json"'
    class_name_a = '"bgpAsP"'
    dn_a = "uni/fabric/bgpInstP-default/as"
    asn_a = "asn".format(bgp_as)
    rn_a = "as"

    level3a = {'dn': dn_a, 'asn': asn_a, 'rn': rn_a}
    level2a = {"attributes": level3a}
    level1a = {'bgpAsP': level2a}
    data_a = level1a

    temp_a = template_m.format(resource_a, "{", path_a, class_name_a, json.dumps(data_a, indent=4), "}")
    wr_base_info.write(temp_a)


def resource_bgp_rr(node_id, line_count, bgp_as, wr_base_info):
    # Validate BGP AS Number
    testvalidator.validate_bgp_as(line_count, bgp_as)

    resource_a = 'resource "aci_rest" "bgp_rr_{}"'.format(node_id)
    path_a = '"/api/node/mo/uni/fabric/bgpInstP-default/rr/node-{}.json"'.format(node_id)
    class_name_a = '"bgpRRNodePEp"'
    dn_a = "uni/fabric/bgpInstP-default/rr/node-{}".format(node_id)
    id_a = node_id
    rn_a = "node-{}".format(node_id)

    level3a = {'dn': dn_a, 'id': id_a, 'rn': rn_a}
    level2a = {'attributes': level3a}
    level1a = {"bgpRRNodePEp": level2a}
    data_a = level1a

    temp_a = template_m.format(resource_a, "{", path_a, class_name_a, json.dumps(data_a, indent=4), "}")
    wr_base_info.write(temp_a)


def resource_dns(dns_ipv4, prefer, line_count, wr_base_info):
    # Validate DNS IPv4 Address
    try:
        testvalidator.validate_ipv4(line_count, dns_ipv4)
    except Exception as err:
        print('\r\r----------------\r')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}, Please verify input information.')
        print('----------------\r\r')
        exit()
    
    dns_ipv4_ = dns_ipv4.replace('.', '_')

    resource_a = 'resource "aci_rest" "dns_{}"'.format(dns_ipv4_)
    path_a = '"api/node/mo/uni/fabric/dnsp-default/prov-[{}].json"'.format(dns_ipv4)
    class_name_a = '"dnsProv"'
    dn_a = "uni/fabric/dnsp-default/prov-[{}]".format(dns_ipv4)
    addr_a = dns_ipv4
    preferred_a = prefer
    rn_a = "prov-[{}]".format(dns_ipv4)
    children_a = []

    level3a = {'dn': dn_a, 'addr': addr_a, 'preferred': preferred_a, 'rn': rn_a}
    level2a = {'attributes': level3a, 'children': children_a}
    level1a = {'dnsProv': level2a}
    data_a = level1a

    temp_a = template_m.format(resource_a, "{", path_a, class_name_a, json.dumps(data_a, indent=4), "}")
    wr_base_info.write(temp_a)


def resource_dns_mgmt(mgmt_domain, line_count, wr_base_info):
    # Validate Management Domain
    mgmt_domain = testvalidator.validate_mgmt_domain(line_count, mgmt_domain)

    resource_a = 'resource "aci_rest" "dns_mgmt"'
    path_a = '"/api/node/mo/uni/fabric/dnsp-default.json"'
    class_name_a = '"dnsRsProfileToEpg"'
    tDn_a = "uni/tn-mgmt/mgmtp-default/{}".format(mgmt_domain)

    level3a = {'tDn': tDn_a}
    level2a = {'attributes': level3a}
    level1a = {'dnsRsProfileToEpg': level2a}
    data_a = level1a

    temp_a = template_m.format(resource_a, "{", path_a, class_name_a, json.dumps(data_a, indent=4), "}")
    wr_base_info.write(temp_a)


def resource_domain(domain, prefer, wr_base_info):
    domain_ = domain.replace('.', '_')

    resource_a = 'resource "aci_rest" "domain_{}"'.format(domain_)
    path_a = '"api/node/mo/uni/fabric/dnsp-default/dom-[{}].json"'.format(domain)
    class_name_a = '"dnsDomain"'
    dn_a = "uni/fabric/dnsp-default/dom-[{}]".format(domain)
    name_a = domain
    isDefault_a = prefer
    rn_a = "dom-[{}]".format(domain)
    children_a = []

    level3a = {'dn': dn_a, 'name': name_a, 'isDefault': isDefault_a, 'rn': rn_a}
    level2a = {'attributes': level3a, 'children': children_a}
    level1a = {'dnsDomain': level2a}
    data_a = level1a

    temp_a = template_m.format(resource_a, "{", path_a, class_name_a, json.dumps(data_a, indent=4), "}")
    wr_base_info.write(temp_a)


# This section would need different templates. Not sure if worth doing... TBD...
def resource_inband(inb_ipv4, inb_gwv4, inb_vlan, line_count):
    
    # Validate Inband VLAN
    try:
        testvalidator.validate_inb_vlan(line_count, inb_vlan)
    except Exception as err:
        print('\r\r----------------\r')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}, Please verify input information.')
        print('----------------\r\r')
        exit()

    pfx = inb_ipv4.split('/', 2)
    gwv4 = str(inb_gwv4) + '/' + str(pfx[1])
    file_inb = ('resources_user_import_Tenant_Mgmt.tf')
    wr_file_inb = open(file_inb, 'w')
    wr_file_inb.write('# Use this Resource File to Register the inband management network for the Fabric\n')

    #wr_file_inb.write('\n')
    wr_file_inb.write('\n''resource "aci_tenant" "mgmt" {\n' )
    wr_file_inb.write('\tname\t= "mgmt"\n')
    wr_file_inb.write('}\n\n')
    #wr_file_inb.write('\n')

    wr_file_inb.write('resource "aci_bridge_domain" "inb" {\n' )
    wr_file_inb.write('\ttenant_dn\t= aci_tenant.mgmt.id\n' )
    wr_file_inb.write('\tname\t= "inb"\n')
    wr_file_inb.write('}\n\n')
    #wr_file_inb.write('\n')

    wr_file_inb.write('resource "aci_subnet" "inb_subnet" {\n' )
    wr_file_inb.write('\tparent_dn\t= aci_bridge_domain.inb.id\n' )
    #wr_file_inb.write('\tip\t= "%s"\n' % (gwv4))
    wr_file_inb.write('\tip\t= "{}"\n'.format(gwv4))
    wr_file_inb.write('\tscope\t= ["public"]\n')
    wr_file_inb.write('}\n\n')
    #wr_file_inb.write('\n')

    wr_file_inb.write('resource "aci_application_profile" "inb_ap" {\n' )
    wr_file_inb.write('\ttenant_dn\t= aci_tenant.mgmt.id\n' )
    wr_file_inb.write('\tname\t= "inb_ap"\n')
    wr_file_inb.write('}\n\n')
    #wr_file_inb.write('\n')

    wr_file_inb.write('resource "aci_application_epg" "inb_epg" {\n' )
    wr_file_inb.write('\tapplication_profile_dn\t= aci_application_profile.inb_ap.id\n' )
    wr_file_inb.write('\tname\t= "inb_epg"\n')
    wr_file_inb.write('\tdescription\t= "Inband Mgmt EPG for APIC and Switch Management"\n')
    wr_file_inb.write('}\n\n')
    #wr_file_inb.write('\n')

    wr_file_inb.write('resource "aci_ranges" "inb_vlan" {\n')
    wr_file_inb.write('\tvlan_pool_dn\t= "uni/infra/vlanns-[inband_vl-pool]-static"\n')
    #wr_file_inb.write('\t_from\t= "vlan-%s"\n' % (inb_vlan))
    wr_file_inb.write('\t_from\t= "vlan-{}"\n'.format(inb_vlan))
    #wr_file_inb.write('\tto\t= "vlan-%s"\n' % (inb_vlan))
    wr_file_inb.write('\tto\t= "vlan-{}"\n'.format(inb_vlan))
    wr_file_inb.write('}\n\n')
    #wr_file_inb.write('\n')

    wr_file_inb.write('resource "aci_rest" "inb_mgmt_default_epg" {\n')
    wr_file_inb.write('\tpath       = "/api/node/mo/uni/tn-mgmt/mgmtp-default/inb-inb_epg.json"\n')
    wr_file_inb.write('\tclass_name = "mgmtInB"\n')
    wr_file_inb.write('\tpayload    = <<EOF\n')
    wr_file_inb.write('{\n')
    wr_file_inb.write('\t"mgmtInB": {\n')
    wr_file_inb.write('\t\t"attributes": {\n')
    wr_file_inb.write('\t\t\t"descr": "",\n')
    wr_file_inb.write('\t\t\t"dn": "uni/tn-mgmt/mgmtp-default/inb-inb_epg",\n')
    wr_file_inb.write('\t\t\t"encap": "vlan-%s",\n' % (inb_vlan))
    wr_file_inb.write('\t\t\t"name": "inb_epg",\n')
    wr_file_inb.write('\t\t},\n')
    wr_file_inb.write('\t\t"children": [\n')
    wr_file_inb.write('\t\t\t{\n')
    wr_file_inb.write('\t\t\t\t"mgmtRsMgmtBD": {\n')
    wr_file_inb.write('\t\t\t\t\t"attributes": {\n')
    wr_file_inb.write('\t\t\t\t\t\t"tnFvBDName": "inb"\n')
    wr_file_inb.write('\t\t\t\t\t}\n')
    wr_file_inb.write('\t\t\t\t}\n')
    wr_file_inb.write('\t\t\t}\n')
    wr_file_inb.write('\t\t]\n')
    wr_file_inb.write('\t}\n')
    wr_file_inb.write('}\n')
    wr_file_inb.write('\tEOF\n')
    wr_file_inb.write('}\n\n')
    #wr_file_inb.write('\n')

    wr_file_inb.close()


# This section would need different templates. Not sure if worth doing... TBD...
def resource_ntp(ntp_ipv4, prefer, mgmt_domain, line_count, wr_base_info):
    # Validate Management Domain
    mgmt_domain = testvalidator.validate_mgmt_domain(line_count, mgmt_domain)
    
    # Validate NTP IPv4 Address
    try:
        testvalidator.validate_ipv4(line_count, ntp_ipv4)
    except Exception as err:
        print('\r\r----------------\r')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}, Please verify {ntp_ipv4} input information.')
        print('----------------\r\r')
        exit()

    ntp_ipv4_ = ntp_ipv4.replace('.', '_')
    wr_base_info.write('resource "aci_rest" "ntp_%s" {\n' % (ntp_ipv4_))
    wr_base_info.write('\tpath       = "/api/node/mo/uni/fabric/time-default/ntpprov-%s.json"\n' % (ntp_ipv4))
    wr_base_info.write('\tclass_name = "datetimeNtpProv"\n')
    wr_base_info.write('\tpayload    = <<EOF\n')
    wr_base_info.write('{\n')
    wr_base_info.write('\t"datetimeNtpProv": {\n')
    wr_base_info.write('\t\t"attributes": {\n')
    wr_base_info.write('\t\t\t"dn": "uni/fabric/time-default/ntpprov-%s",\n' % (ntp_ipv4))
    wr_base_info.write('\t\t\t"name": "%s",\n' % (ntp_ipv4))
    wr_base_info.write('\t\t\t"preferred": "%s",\n' % (prefer))
    wr_base_info.write('\t\t\t"rn": "ntpprov-%s",\n' % (ntp_ipv4))
    wr_base_info.write('\t\t},\n')
    wr_base_info.write('\t\t"children": [\n')
    wr_base_info.write('\t\t\t{\n')
    wr_base_info.write('\t\t\t\t"datetimeRsNtpProvToEpg": {\n')
    wr_base_info.write('\t\t\t\t\t"attributes": {\n')
    wr_base_info.write('\t\t\t\t\t\t"tDn": "uni/tn-mgmt/mgmtp-default/%s",\n' % (mgmt_domain))
    wr_base_info.write('\t\t\t\t\t}\n')
    wr_base_info.write('\t\t\t\t}\n')
    wr_base_info.write('\t\t\t}\n')
    wr_base_info.write('\t\t]\n')
    wr_base_info.write('\t}\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\tEOF\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\n')


def resource_snmp_client(client_name, client_ipv4, mgmt_domain, line_count, wr_base_info):
    # Validate Management Domain
    snmp_mgmt = testvalidator.validate_snmp_mgmt(line_count, mgmt_domain)
    
    # Validate SNMP IPv4 Client Address
    try:
        testvalidator.validate_ipv4(line_count, client_ipv4)
    except Exception as err:
        print('\r\r----------------\r')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}, Please verify {client_ipv4} input information.')
        print('----------------\r\r')
        exit()

    client_ipv4_ = client_ipv4.replace('.', '_')

    resource_a = 'resource "aci_rest" "snmp_client_{}"'.format(client_ipv4_)
    path_a = '"/api/node/mo/uni/fabric/snmppol-default/clgrp-{}_Clients/client-[{}].json"'.format(snmp_mgmt, client_ipv4)
    class_name_a = '"snmpClientP"'
    dn_a = "uni/fabric/snmppol-default/clgrp-{}_Clients/client-[{}]".format(snmp_mgmt, client_ipv4)
    name_a = client_name
    addr_a = client_ipv4
    rn_a = "client-{}".format(client_ipv4)
    children_a = []

    level3a = {'dn': dn_a, 'name': name_a, 'addr': addr_a, 'rn': rn_a}
    level2a = {'attributes': level3a, 'children': children_a}
    level1a = {'snmpClientP': level2a}
    data_a = level1a

    temp_a = template_m.format(resource_a, "{", path_a, class_name_a, json.dumps(data_a, indent=4), "}")
    wr_base_info.write(temp_a)


# BREAK
def resource_snmp_comm(community, description, wr_base_info):

    wr_base_info.write('resource "aci_rest" "snmp_comm_%s" {\n' % (community))
    wr_base_info.write('\tpath       = "/api/node/mo/uni/fabric/snmppol-default/community-%s.json"\n' % (community))
    wr_base_info.write('\tclass_name = "snmpCommunityP"\n')
    wr_base_info.write('\tpayload    = <<EOF\n')
    wr_base_info.write('{\n')
    wr_base_info.write('\t"snmpCommunityP": {\n')
    wr_base_info.write('\t\t"attributes": {\n')
    wr_base_info.write('\t\t\t"dn": "uni/fabric/snmppol-default/community-%s",\n' % (community))
    wr_base_info.write('\t\t\t"descr": "%s",\n' % (description))
    wr_base_info.write('\t\t\t"name": "%s",\n' % (community))
    wr_base_info.write('\t\t\t"rn": "community-%s"\n' % (community))
    wr_base_info.write('\t\t},\n')
    wr_base_info.write('\t\t"children": []\n')
    wr_base_info.write('\t}\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\tEOF\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\n')


def resource_snmp_info(contact, location, wr_base_info):
    wr_base_info.write('resource "aci_rest" "snmp_info" {\n')
    wr_base_info.write('\tpath       = "/api/node/mo/uni/fabric/snmppol-default.json"\n')
    wr_base_info.write('\tclass_name = "snmpPol"\n')
    wr_base_info.write('\tpayload    = <<EOF\n')
    wr_base_info.write('{\n')
    wr_base_info.write('\t"snmpPol": {\n')
    wr_base_info.write('\t\t"attributes": {\n')
    wr_base_info.write('\t\t\t"dn": "uni/fabric/snmppol-default",\n')
    wr_base_info.write('\t\t\t"descr": "This is the default SNMP Policy",\n')
    wr_base_info.write('\t\t\t"adminSt": "enabled",\n')
    wr_base_info.write('\t\t\t"contact": "%s",\n' % (contact))
    wr_base_info.write('\t\t\t"loc": "%s",\n' % (location))
    wr_base_info.write('\t\t},\n')
    wr_base_info.write('\t\t"children": []\n')
    wr_base_info.write('\t}\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\tEOF\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\n')


def resource_snmp_trap(snmp_ipv4, snmp_port, line_count, wr_base_info):
    
    # Validate SNMP Trap Server IPv4 Address
    try:
        testvalidator.validate_ipv4(line_count, snmp_ipv4)
    except Exception as err:
        print('\r\r----------------\r')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}, Please verify {snmp_ipv4} input information.')
        print('----------------\r\r')
        exit()

    snmp_ipv4_ = snmp_ipv4.replace('.', '_')
    wr_base_info.write('resource "aci_rest" "snmp_trap_%s" {\n' % (snmp_ipv4_))
    wr_base_info.write('\tpath       = "api/node/mo/uni/fabric/snmppol-default/trapfwdserver-[%s].json"\n' % (snmp_ipv4))
    wr_base_info.write('\tclass_name = "snmpTrapFwdServerP"\n')
    wr_base_info.write('\tpayload    = <<EOF\n')
    wr_base_info.write('{\n')
    wr_base_info.write('\t"snmpTrapFwdServerP": {\n')
    wr_base_info.write('\t\t"attributes": {\n')
    wr_base_info.write('\t\t\t"addr": "%s",\n' % (snmp_ipv4))
    if not snmp_port == '':
        wr_base_info.write('\t\t\t"port": "%s",\n' % (snmp_port))
    wr_base_info.write('\t\t},\n')
    wr_base_info.write('\t\t"children": []\n')
    wr_base_info.write('\t}\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\tEOF\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\n')


def resource_snmp_user(snmp_user, priv_type, priv_key, auth_type, auth_key, line_count, wr_base_info):
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
    wr_base_info.write('resource "aci_rest" "snmp_user_%s" {\n' % (snmp_user))
    wr_base_info.write('\tpath       = "/api/node/mo/uni/fabric/snmppol-default/user-%s.json"\n' % (snmp_user))
    wr_base_info.write('\tclass_name = "snmpUserP"\n')
    wr_base_info.write('\tpayload    = <<EOF\n')
    wr_base_info.write('{\n')
    wr_base_info.write('\t"snmpUserP": {\n')
    wr_base_info.write('\t\t"attributes": {\n')
    if not priv_type == '':
        wr_base_info.write('\t\t\t"privType": "%s",\n' % (priv_type))
        wr_base_info.write('\t\t\t"privKey": "%s",\n' % (priv_key))
    wr_base_info.write('\t\t\t"authKey": "%s",\n' % (auth_key))
    if not auth_type == '':
        wr_base_info.write('\t\t\t"authType": "%s",\n' % (auth_type))
    wr_base_info.write('\t\t\t"name": "%s",\n' % (snmp_user))
    wr_base_info.write('\t\t},\n')
    wr_base_info.write('\t\t"children": []\n')
    wr_base_info.write('\t}\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\tEOF\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\n')


# Different Template is needed... TBD....
def resource_switch(serial, name, node_id, node_type, pod_id, switch_role, modules, port_count, oob_ipv4, oob_gwv4, inb_ipv4, inb_gwv4, inb_vlan, line_count):
    try:
        # Validate Serial Number
        
        # Validate Hostname
        testvalidator.validate_hostname(line_count, name)
        
        # Validate Node_ID
        testvalidator.validate_node_id(line_count, name, node_id)

        # Validate node_type
        testvalidator.validate_node_type(line_count, name, node_type)

        # Validate Pod_ID
        testvalidator.validate_pod_id(line_count, name, pod_id)

        # Validate switch role
        testvalidator.validate_role(line_count, name, switch_role)

        # Validate Modules
        testvalidator.validate_modules(line_count, name, switch_role, modules)

        # Validate port_count
        testvalidator.validate_port_count(line_count, name, switch_role, port_count)

        # Validate InBand Network
        testvalidator.validate_inband(line_count, name, inb_ipv4, inb_gwv4)

        # Validate Out-of-Band Network
        testvalidator.validate_oob(line_count, name, oob_ipv4, oob_gwv4)

    except Exception as err:
        print('\r\r----------------\r')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}, Please verify input information.')
        print('----------------\r\r')
        exit()

    notes = f'# Use this Resource File to Register {name} with node id {node_id} to the Fabric\n' \
            '# Requirements are:\n'\
            '# serial: Actual Serial Number of the switch.\n'\
            '# name: Hostname you want to assign.\n' \
            '# node_id: unique ID used to identify the switch in the APIC.\n' \
            '#   in the "Cisco ACI Object Naming and Numbering: Best Practice\n' \
            '#   The recommendation is that the Spines should be 101-199\n' \
            '#   and leafs should start at 200+ thru 4000.  As the number of\n' \
            '#   spines should always be less than the number of leafs\n' \
            '#   https://www.cisco.com/c/en/us/td/docs/switches/datacenter/aci/apic/sw/' \
            'kb/b-Cisco-ACI-Naming-and-Numbering.html#id_107280\n' \
            '# node_type: uremote-leaf-wan or unspecified.\n' \
            '# role: spine, leaf.\n' \
            '# pod_id: Typically this will be one unless you are running multipod.\n'

    pod_id = str(pod_id)
    file_sw = 'resources_user_import_xDevice_{}.tf'.format(name)
    wr_file_sw = open(file_sw, 'w')
    wr_file_sw.write(notes + '\n')

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
    wr_file_sw.write('resource "aci_rest" "inb_mgmt_%s" {\n' % (name))
    wr_file_sw.write('\tpath       = "/api/node/mo/uni/tn-mgmt.json"\n')
    wr_file_sw.write('\tclass_name = "mgmtRsInBStNode"\n')
    wr_file_sw.write('\tpayload    = <<EOF\n')
    wr_file_sw.write('{\n')
    wr_file_sw.write('\t"mgmtRsInBStNode": {\n')
    wr_file_sw.write('\t\t"attributes": {\n')
    wr_file_sw.write('\t\t\t"addr":"%s",\n' % (inb_ipv4))
    wr_file_sw.write('\t\t\t"dn":"uni/tn-mgmt/mgmtp-default/inb-inb_epg/rsinBStNode-[topology/pod-%s/node-%s]",\n' % (pod_id, node_id))
    wr_file_sw.write('\t\t\t"gw":"%s",\n' % (inb_gwv4))
    wr_file_sw.write('\t\t\t"tDn":"topology/pod-%s/node-%s",\n' % (pod_id, node_id))
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

