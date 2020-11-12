import csv
import ipaddress
import re, sys, traceback, validators

if len(sys.argv) == 2:
    csv_input = sys.argv[1]
    append = sys.argv[1]
elif len(sys.argv) == 1:
    csv_input = sys.argv[1]
    append = 'no'

file_base_pod_info = 'resources_user_import_base_pod_policies.tf'

if append == 'yes':
    wr_base_info = open(file_base_pod_info, 'a')
else:
    wr_base_info = open(file_base_pod_info, 'w')
    wr_base_info.write('# This File will include DNS, Domain, NTP, Timezone and other base configuration parameters\n')

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

def resource_apic_inb(name, node_id, pod_id, inb_ipv4, inb_gwv4, inb_vlan, p1_leaf, p1_swpt, p2_leaf, p2_swpt):
    try:
        # Validate APIC Node_ID
        validate_node_id_apic(line_count, name, node_id)

        # Validate Pod_ID
        validate_pod_id(line_count, name, pod_id)

        # Validate InBand Network
        validate_inband(line_count, name, inb_ipv4, inb_gwv4)
    except Exception as err:
        print('\r\r----------------\r')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}, Please verify input information.')
        print('----------------\r\r')
        exit()
    pod_id = str(pod_id)
    file_apic = ('resources_user_import_%s.tf' % (name))
    wr_apic = open(file_apic, 'w')
    wr_apic.write('resource "aci_rest" "inb_mgmt_apic_%s" {\n' % (name))
    wr_apic.write('\tpath       = "/api/node/mo/uni/tn-mgmt.json"\n')
    wr_apic.write('\tclass_name = "mgmtRsInBStNode"\n')
    wr_apic.write('\tpayload    = <<EOF\n')
    wr_apic.write('{\n')
    wr_apic.write('\t"mgmtRsInBStNode": {\n')
    wr_apic.write('\t\t"attributes": {\n')
    wr_apic.write('\t\t\t"addr":"%s",\n' % (inb_ipv4))
    wr_apic.write('\t\t\t"dn":"uni/tn-mgmt/mgmtp-default/inb-inb_epg/rsinBStNode-[topology/pod-%s/node-%s]",\n' % (pod_id, node_id))
    wr_apic.write('\t\t\t"gw":"%s",\n' % (inb_gwv4))
    wr_apic.write('\t\t\t"tDn":"topology/pod-%s/node-%s",\n' % (pod_id, node_id))
    wr_apic.write('\t\t}\n')
    wr_apic.write('\t}\n')
    wr_apic.write('}\n')
    wr_apic.write('\tEOF\n')
    wr_apic.write('}\n')
    wr_apic.write('\n')
    # resource_apic_inb(name, node_id, pod_id, inb_ipv4, inb_gwv4, inb_vlan, p1_leaf, p1_swpt, p2_leaf, p2_swpt):
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
        wr_apic.write('resource "aci_rest" "%s_port_2_%s" {\n' % (name, port_list_count))
        wr_apic.write('\tpath       = "/api/node/mo/uni/infra/accportprof-%s_IntProf/hports-Eth%s-%s-typ-range/rsaccBaseGrp.json"\n'% (leaf, module, port))
        wr_apic.write('\tclass_name = "infraRsAccBaseGrp"\n')
        wr_apic.write('\tpayload    = <<EOF\n')
        wr_apic.write('{\n')
        wr_apic.write('\t"infraRsAccBaseGrp": {\n')
        wr_apic.write('\t\t"attributes": {\n')
        wr_apic.write('\t\t\t"tDn": "uni/infra/funcprof/accportgrp-inband_ap",\n')
        wr_apic.write('\t\t}\n')
        wr_apic.write('\t}\n')
        wr_apic.write('}\n')
        wr_apic.write('\tEOF\n')
        wr_apic.write('}\n')
        wr_apic.write('\n')
    wr_apic.close()


def resource_bgp_as(bgp_as):
    # Validate BGP AS Number
    validate_bgp_as(line_count, bgp_as)
        
    wr_base_info.write('resource "aci_rest" "bgp_as" {\n')
    wr_base_info.write('\tpath       = "/api/node/mo/uni/fabric/bgpInstP-default/as.json"\n')
    wr_base_info.write('\tclass_name = "bgpAsP"\n')
    wr_base_info.write('\tpayload    = <<EOF\n')
    wr_base_info.write('{\n')
    wr_base_info.write('\t"bgpAsP": {\n')
    wr_base_info.write('\t\t"attributes": {\n')
    wr_base_info.write('\t\t\t"dn": "uni/fabric/bgpInstP-default/as",\n')
    wr_base_info.write('\t\t\t"asn": "%s",\n' % (bgp_as))
    wr_base_info.write('\t\t\t"rn": "as"\n')
    wr_base_info.write('\t\t}\n')
    wr_base_info.write('\t}\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\tEOF\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\n')

def resource_bgp_rr(node_id):
    # Validate BGP AS Number
    validate_bgp_as(line_count, bgp_as)
        
    wr_base_info.write('resource "aci_rest" "bgp_rr_%s" {\n' % (node_id))
    wr_base_info.write('\tpath       = "/api/node/mo/uni/fabric/bgpInstP-default/rr/node-%s.json"\n' % (node_id))
    wr_base_info.write('\tclass_name = "bgpRRNodePEp"\n')
    wr_base_info.write('\tpayload    = <<EOF\n')
    wr_base_info.write('{\n')
    wr_base_info.write('\t"bgpRRNodePEp": {\n')
    wr_base_info.write('\t\t"attributes": {\n')
    wr_base_info.write('\t\t\t"dn": "uni/fabric/bgpInstP-default/rr/node-%s",\n' % (node_id))
    wr_base_info.write('\t\t\t"id": "%s",\n' % (node_id))
    wr_base_info.write('\t\t\t"rn": "node-%s"\n' % (node_id))
    wr_base_info.write('\t\t}\n')
    wr_base_info.write('\t}\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\tEOF\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\n')

def resource_dns(dns_ipv4, prefer):
    # Validate DNS IPv4 Address
    try:
        validate_ipv4(line_count, dns_ipv4)
    except Exception as err:
        print('\r\r----------------\r')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}, Please verify input information.')
        print('----------------\r\r')
        exit()
    
    dns_ipv4_ = dns_ipv4.replace('.', '_')
    wr_base_info.write('resource "aci_rest" "dns_%s" {\n' % (dns_ipv4_))
    wr_base_info.write('\tpath       = "api/node/mo/uni/fabric/dnsp-default/prov-[%s].json"\n' % (dns_ipv4))
    wr_base_info.write('\tclass_name = "dnsProv"\n')
    wr_base_info.write('\tpayload    = <<EOF\n')
    wr_base_info.write('{\n')
    wr_base_info.write('\t"dnsProv": {\n')
    wr_base_info.write('\t\t"attributes": {\n')
    wr_base_info.write('\t\t\t"dn": "uni/fabric/dnsp-default/prov-[%s]",\n' % (dns_ipv4))
    wr_base_info.write('\t\t\t"addr": "%s",\n' % (dns_ipv4))
    wr_base_info.write('\t\t\t"preferred": "%s",\n' % (prefer))
    wr_base_info.write('\t\t\t"rn": "prov-[%s]"\n' % (dns_ipv4))
    wr_base_info.write('\t\t},\n')
    wr_base_info.write('\t\t"children": []\n')
    wr_base_info.write('\t}\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\tEOF\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\n')

def resource_dns_mgmt(mgmt_domain):
    # Validate Management Domain
    mgmt_domain = validate_mgmt_domain(line_count, mgmt_domain)
        
    wr_base_info.write('resource "aci_rest" "dns_mgmt" {\n')
    wr_base_info.write('\tpath       = "/api/node/mo/uni/fabric/dnsp-default.json"\n')
    wr_base_info.write('\tclass_name = "dnsRsProfileToEpg"\n')
    wr_base_info.write('\tpayload    = <<EOF\n')
    wr_base_info.write('{\n')
    wr_base_info.write('\t"dnsRsProfileToEpg": {\n')
    wr_base_info.write('\t\t"attributes": {\n')
    wr_base_info.write('\t\t\t"tDn": "uni/tn-mgmt/mgmtp-default/%s",\n' % (mgmt_domain))
    wr_base_info.write('\t\t}\n')
    wr_base_info.write('\t}\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\tEOF\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\n')

def resource_domain(domain, prefer):

    domain_ = domain.replace('.', '_')
    wr_base_info.write('resource "aci_rest" "domain_%s" {\n' % (domain_))
    wr_base_info.write('\tpath       = "api/node/mo/uni/fabric/dnsp-default/dom-[%s].json"\n' % (domain))
    wr_base_info.write('\tclass_name = "dnsDomain"\n')
    wr_base_info.write('\tpayload    = <<EOF\n')
    wr_base_info.write('{\n')
    wr_base_info.write('\t"dnsDomain": {\n')
    wr_base_info.write('\t\t"attributes": {\n')
    wr_base_info.write('\t\t\t"dn": "uni/fabric/dnsp-default/dom-[%s]",\n' % (domain))
    wr_base_info.write('\t\t\t"name": "%s",\n' % (domain))
    wr_base_info.write('\t\t\t"isDefault": "%s",\n' % (prefer))
    wr_base_info.write('\t\t\t"rn": "dom-[%s]"\n' % (domain))
    wr_base_info.write('\t\t},\n')
    wr_base_info.write('\t\t"children": []\n')
    wr_base_info.write('\t}\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\tEOF\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\n')

def resource_inband(inb_ipv4, inb_gwv4, inb_vlan):
    
    # Validate Inband VLAN
    try:
        validate_inb_vlan(line_count, inb_vlan)
    except Exception as err:
        print('\r\r----------------\r')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}, Please verify input information.')
        print('----------------\r\r')
        exit()

    pfx = inb_ipv4.split('/', 2)
    gwv4 = str(inb_gwv4) + '/' + str(pfx[1])
    file_inb = ('resources_from_user_tenant_mgmt.tf')
    wr_file_inb = open(file_inb, 'w')
    wr_file_inb.write('# Use this Resource File to Register the inband management network for the Fabric\n')
    wr_file_inb.write('\n')
    wr_file_inb.write('resource "aci_tenant" "mgmt" {\n' )
    wr_file_inb.write('\tname                   = "mgmt"\n')
    wr_file_inb.write('}\n')
    wr_file_inb.write('\n')
    wr_file_inb.write('resource "aci_bridge_domain" "inb" {\n' )
    wr_file_inb.write('\ttenant_dn = aci_tenant.mgmt.id\n' )
    wr_file_inb.write('\tname                   = "inb"\n')
    wr_file_inb.write('}\n')
    wr_file_inb.write('\n')
    wr_file_inb.write('resource "aci_subnet" "inb_subnet" {\n' )
    wr_file_inb.write('\tparent_dn              = aci_bridge_domain.inb.id\n' )
    wr_file_inb.write('\tip                   = "%s"\n' % (gwv4))
    wr_file_inb.write('\tscope                  = ["public"]\n')
    wr_file_inb.write('}\n')
    wr_file_inb.write('\n')
    wr_file_inb.write('resource "aci_application_profile" "inb_ap" {\n' )
    wr_file_inb.write('\ttenant_dn              = aci_tenant.mgmt.id\n' )
    wr_file_inb.write('\tname                   = "inb_ap"\n')
    wr_file_inb.write('}\n')
    wr_file_inb.write('\n')
    wr_file_inb.write('resource "aci_application_epg" "inb_epg" {\n' )
    wr_file_inb.write('\tapplication_profile_dn = aci_application_profile.inb_ap.id\n' )
    wr_file_inb.write('\tname                   = "inb_epg"\n')
    wr_file_inb.write('\tdescription            = "Inband Mgmt EPG for APIC and Switch Management"\n')
    wr_file_inb.write('}\n')
    wr_file_inb.write('\n')
    wr_file_inb.write('resource "aci_ranges" "inb_vlan" {\n')
    wr_file_inb.write('vlan_pool_dn	= "uni/infra/vlanns-[inband_vl-pool]-static"\n')
    wr_file_inb.write('_from		= "vlan-%s"\n' % (inb_vlan))
    wr_file_inb.write('to		= "vlan-%s"\n' % (inb_vlan))
    wr_file_inb.write('}\n')
    wr_file_inb.write('\n')
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
    wr_file_inb.write('}\n')
    wr_file_inb.write('\n')
    wr_file_inb.close()


def resource_ntp(ntp_ipv4, prefer, mgmt_domain):
    # Validate Management Domain
    mgmt_domain = validate_mgmt_domain(line_count, mgmt_domain)
    
    # Validate NTP IPv4 Address
    try:
        validate_ipv4(line_count, ntp_ipv4)
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

def resource_snmp_client(client_name, client_ipv4, mgmt_domain):
    # Validate Management Domain
    snmp_mgmt = validate_snmp_mgmt(line_count, mgmt_domain)
    
    # Validate SNMP IPv4 Client Address
    try:
        validate_ipv4(line_count, client_ipv4)
    except Exception as err:
        print('\r\r----------------\r')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}, Please verify {client_ipv4} input information.')
        print('----------------\r\r')
        exit()

    client_ipv4_ = client_ipv4.replace('.', '_')
    wr_base_info.write('resource "aci_rest" "snmp_client_%s" {\n' % (client_ipv4_))
    wr_base_info.write('\tpath       = "/api/node/mo/uni/fabric/snmppol-default/clgrp-%s_Clients/client-[%s].json"\n' % (snmp_mgmt, client_ipv4))
    wr_base_info.write('\tclass_name = "snmpClientP"\n')
    wr_base_info.write('\tpayload    = <<EOF\n')
    wr_base_info.write('{\n')
    wr_base_info.write('\t"snmpClientP": {\n')
    wr_base_info.write('\t\t"attributes": {\n')
    wr_base_info.write('\t\t\t"dn": "uni/fabric/snmppol-default/clgrp-%s_Clients/client-[%s]",\n' % (snmp_mgmt, client_ipv4))
    wr_base_info.write('\t\t\t"name": "%s",\n' % (client_name))
    wr_base_info.write('\t\t\t"addr": "%s",\n' % (client_ipv4))
    wr_base_info.write('\t\t\t"rn": "client-%s",\n' % (client_ipv4))
    wr_base_info.write('\t\t},\n')
    wr_base_info.write('\t\t"children": []\n')
    wr_base_info.write('\t}\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\tEOF\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\n')

def resource_snmp_comm(community, description):
    wr_base_info.write('resource "aci_rest" "snmp_comm_%s" {\n' % (community))
    wr_base_info.write('\tpath       = "/api/node/mo/uni/fabric/snmppol-default/community-%s.json"\n' % (community))
    wr_base_info.write('\tclass_name = "snmpCommunityP"\n')
    wr_base_info.write('\tpayload    = <<EOF\n')
    wr_base_info.write('{\n')
    wr_base_info.write('\t"snmpCommunityP": {\n')
    wr_base_info.write('\t\t"attributes": {\n')
    wr_base_info.write('\t\t\t"dn": "uni/fabric/snmppol-default/community%s",\n' % (community))
    wr_base_info.write('\t\t\t"descr": "%s",\n' % (description))
    wr_base_info.write('\t\t\t"name": "%s",\n' % (community))
    wr_base_info.write('\t\t\t"rn": "community%s"\n' % (community))
    wr_base_info.write('\t\t},\n')
    wr_base_info.write('\t\t"children": []\n')
    wr_base_info.write('\t}\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\tEOF\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\n')

def resource_snmp_info(contact, location):
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

def resource_snmp_user(community, description):
    wr_base_info.write('resource "aci_rest" "snmp_comm_%s" {\n' % (community))
    wr_base_info.write('\tpath       = "/api/node/mo/uni/fabric/snmppol-default/community-%s.json"\n' % (community))
    wr_base_info.write('\tclass_name = "snmpCommunityP"\n')
    wr_base_info.write('\tpayload    = <<EOF\n')
    wr_base_info.write('{\n')
    wr_base_info.write('\t"snmpCommunityP": {\n')
    wr_base_info.write('\t\t"attributes": {\n')
    wr_base_info.write('\t\t\t"dn": "uni/fabric/snmppol-default/community%s",\n' % (community))
    wr_base_info.write('\t\t\t"descr": "%s",\n' % (description))
    wr_base_info.write('\t\t\t"name": "%s",\n' % (community))
    wr_base_info.write('\t\t\t"rn": "community%s"\n' % (community))
    wr_base_info.write('\t\t},\n')
    wr_base_info.write('\t\t"children": []\n')
    wr_base_info.write('\t}\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\tEOF\n')
    wr_base_info.write('}\n')
    wr_base_info.write('\n')

def resource_switch(serial, name, node_id, node_type, pod_id, switch_role, modules, port_count, oob_ipv4, oob_gwv4, inb_ipv4, inb_gwv4, inb_vlan):
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
            elif type == 'Company':
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
            elif type == 'snmp_client':
                client_name = column[1]
                client_ipv4 = column[2]
                mgmt_domain = column[3]
                # Create Resource Record for SNMP Client
                resource_snmp_client(client_name, client_ipv4, mgmt_domain)
                line_count += 1
            elif type == 'snmp_info':
                contact = column[1]
                location = column[2]
                # Create Resource Record for SNMP Default Policy
                resource_snmp_info(contact, location)
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
wr_base_info.close()

#End Script
print('\r\r----------------\r')
print(f'  Completed Running Script')
print(f'  Exiting...')
print('----------------\r\r')
exit()