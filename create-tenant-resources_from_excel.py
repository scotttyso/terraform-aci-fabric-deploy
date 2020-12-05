#!/usr/bin/env python3

import aci
import getpass
import ipaddress
import json
import phonenumbers
import openpyxl
import os, re, sys, traceback, validators
import requests
import tf_templates
import urllib3
import validating
from datetime import datetime, timedelta
from openpyxl import load_workbook,workbook
from os import path


excel_workbook = sys.argv[1]
try:
    if os.path.isfile(excel_workbook):
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {excel_workbook} exists.  Beginning Script Execution...')
        print(f'\n-----------------------------------------------------------------------------\n')
    else:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {excel_workbook} does not exist.  Exiting....')
        print(f'\n-----------------------------------------------------------------------------\n')
        exit()
except IOError:
    print(f'\n-----------------------------------------------------------------------------\n')
    print(f'   {excel_workbook} does not exist.  Exiting....')
    print(f'\n-----------------------------------------------------------------------------\n')
    exit()
wb = load_workbook(excel_workbook)
ws1 = wb['Tenant']
ws2 = wb['VRF']
ws3 = wb['L3Out']
ws4 = wb['Bridge Domain']
ws5 = wb['Subnet']
ws6 = wb['DHCP Relay']
ws7 = wb['App and EPGs']
ws8 = wb['Access Interfaces']

# Create Resource configuration Files to store user input Data
# resources_user_import_tntv.tf will include Tenant and VRF Definitions
# resources_user_import_bds.tf will include Bridge Domains, DHCP Relay and Subnets
# resources_user_import_epgs.tf will include Apps and EPGs
# resources_user_import_intf.tf
file_apps = './fabric/resources_user_import_apps.tf'
file_bds = './fabric/resources_user_import_bds.tf'
file_epgs = './fabric/resources_user_import_epgs.tf'
file_portgps = './fabric/resources_user_import_int_portgrps.tf'
file_tenants = './fabric/resources_user_input_Tenants.tf'
file_vrfs = './fabric/resources_user_input_VRFs.tf'
file_vlans = './fabric/resources_user_input_VLANs.tf'
wr_apps = open(file_apps, 'w+')
wr_epgs = open(file_epgs, 'w+')
wr_bds = open(file_bds, 'w+')
wr_portgps = open(file_portgps, 'w+')
wr_tenants = open(file_tenants, 'w')
wr_vrfs = open(file_vrfs, 'w')
wr_vlans = open(file_vlans, 'w+')
#wr_apps.write('# This File will include Applications\n\nvariable \"user_apps\" {\n\tdefault = {\n')
wr_apps.write('# This File will include Applications\n\n')
wr_epgs.write('# This File will include EPGs\n\n')
wr_bds.write('# This File will include Bridge Domains\n\n')
wr_portgps.write('# This File will include Port Group Confgiuration and Mapping\n\n')
wr_tenants.write("# This File will include Tenants\n\n")
wr_vrfs.write("# This File will include VRFs\n\n")

def add_epg_and_vlan(add_type, pod, switch_ipr, node_id, int_select, port, epg, vlan, vl_mode, afile):
    wr_epgs.seek(0)
    if epg in wr_epgs.read():
        wr_vlans.seek(0)
        vl = 'st_vlan_pool_add_%s' % (vlan)
        if not vl in wr_vlans.read():
            st_vlan_pool(vlan, wr_vlans)
        st_to_epg = '%s_%s_%s' % (switch_ipr, int_select, epg)
        afile.seek(0)
        if not st_to_epg in afile.read():
            port_static_path(add_type, pod, switch_ipr, node_id, int_select, port, epg, vlan, vl_mode, afile)

def apic_login():
    #APICIP = None
    #APICUSER = None
    #APICPASS = None
    #APICIP = 'brahma-apic2.rich.ciscolabs.com'
    #APICUSER = 'admin'
    #APICPASS = 'cisco123'
    #
    ## Disable urllib3 warnings
    #urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    #
    ## Prompt for APIC IP if the constant is None
    #if APICIP is not None:
    #    apic = APICIP
    #else:
    #    while True:
    #        apic = input('Enter the APIC IP: ')
    #        try:
    #            ipaddress.ip_address(apic)
    #            break
    #        except Exception as e:
    #            print('Enter a valid IP address. Error received: {}'.format(e))
    #
    ## Prompt for APIC Username if the constant is None
    #if APICUSER is not None:
    #    user = APICUSER
    #else:
    #    user = input('Enter APIC username: ')
    #
    ## Prompt for APIC Password if the constant is None
    #if APICPASS is not None:
    #    pword = APICPASS
    #else:
    #    while True:
    #        try:
    #            pword = getpass.getpass(prompt='Enter APIC password: ')
    #            break
    #        except Exception as e:
    #            print('Something went wrong. Error received: {}'.format(e))
    #
    ## Initialize the fabric login method, passing appropriate variables
    #fablogin = aci.FabLogin(apic, user, pword)
    ## Run the login and load the cookies var
    #cookies = fablogin.login()
    #def get_apg(pg_name):
    #    pg_url = 'https://brahma-apic2/api/node/mo/uni/infra/funcprof/accportgrp-%s' % pg_name
    print('hello world')

def assign_int_descr(switch_ipr, int_select, wr_file):
    wr_file.seek(0) # Read the file from the beginning
    pblock_descr = '%s_%s_descr' % (switch_ipr, int_select)
    if not pblock_descr in wr_file.read():
        x = int_select.split('-')
        xcount = len(x)
        if xcount == 2:
            wr_file.write('resource "aci_access_port_block" "%s_%s_descr" {\n' % (switch_ipr, int_select))
            wr_file.write('\taccess_port_selector_dn    = "uni/infra/accportprof-%s/hports-%s-typ-range"\n' % (switch_ipr, int_select))
            wr_file.write('\tdescription                = "%s"\n' % (descr))
            wr_file.write('}\n\n')
        elif xcount == 3:
            wr_file.write('resource "aci_access_sub_port_block" "%s_%s_descr" {\n' % (switch_ipr, int_select))
            wr_file.write('\tdepends_on                 = [aci_access_sub_port_block.%s_%s]\n' % (switch_ipr, int_select))
            wr_file.write('\taccess_port_selector_dn    = aci_access_port_selector.%s_%s.id\n' % (switch_ipr, int_select))
            wr_file.write('\tdescription                = "%s"\n' % (descr))
            wr_file.write('\tname                       = "block2"\n')
            wr_file.write('}\n\n')

def convert_selector_to_port(int_select):
    xa = int_select.replace('Eth', 'eth')
    xa = xa.replace('-', '/')
    xb = xa.split('/')
    xcount = len(xb)
    if xcount == 3:
        if re.search('^00', xb[2]):
            xc = xb[2].replace('00', '', 1)
            port = '%s/%s/%s' % (xb[0], xb[1], xc)
        elif re.search('^0', xb[2]):
            xc = xb[2].replace('0', '', 1)
            port = '%s/%s/%s' % (xb[0], xb[1], xc)
        else:
            port = xa
    elif xcount == 2:
        if re.search('^00', xb[1]):
            xc = xb[1].replace('00', '', 1)
            port = '%s/%s' % (xb[0], xc)
        elif re.search('^0', xb[1]):
            xc = xb[1].replace('0', '', 1)
            port = '%s/%s' % (xb[0], xc)
        else:
            port = xa
    return port

def net_centric_epg(tenant, bd_name, epg, enforcement, descr, wr_file):
    wr_file.write('resource "aci_application_epg" "%s" {\n' % (epg))
    wr_file.write('\tdepends_on              = [aci_application_profile.%s_nets]\n' % (tenant))
    wr_file.write('\tapplication_profile_dn = aci_application_profile.%s_nets.id\n' % (tenant))
    wr_file.write('\tname                   = "%s"\n' % (epg))
    wr_file.write('\tdescription            = "%s"\n' % (descr))
    wr_file.write('\tflood_on_encap         = "disabled"\n')
    #wr_file.write('\tfwd_ctrl               = "none"\n')
    wr_file.write('\thas_mcast_source       = "no"\n')
    wr_file.write('\tis_attr_based_epg      = "no"\n')
    wr_file.write('\tmatch_t                = "AtleastOne"\n')
    wr_file.write('\tpc_enf_pref            = "enforced"\n')
    if enforcement == 'pg':
        wr_file.write('\tpref_gr_memb           = "include"\n')
    wr_file.write('\tprio                   = "unspecified"\n')
    wr_file.write('\tshutdown               = "no"\n')
    wr_file.write('\trelation_fv_rs_bd      = aci_bridge_domain.%s.id\n' % (bd_name))
    wr_file.write('}\n\n')

def pg_to_int_select(switch_ipr, int_select, rtDn, wr_file):
    # Define Variables for Template Creation - Policy Group to Interface Selector
    # Fabric > Access Policies > Interfaces > Leaf Interfaces > Profiles > {Leaf Interface Profile} > Port Selector
    resrc_desc = '%s_%s_pg' % (switch_ipr, int_select)
    class_name = 'infraRsAccBaseGrp'
    tDn_string = 'uni/infra/funcprof/%s' % (rtDn)
    path_attrs = '/api/node/mo/uni/infra/accportprof-%s/hports-%s-typ-range/rsaccBaseGrp.json' % (switch_ipr, int_select)

    # Format Variables for JSON Output
    data_out = {class_name: {'attributes': {'tDn': tDn_string}, 'children': []}}

    # Write Output to Resource Files using Template
    tf_templates.aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file)

def port_static_path(add_type, pod, switch_ipr, node_id, int_select, port, epg, vlan, vl_mode, afile):
    if add_type == 'add_apg':
        tDn = 'topology/pod-%s/paths-%s/pathep-[%s]' % (pod, node_id, port)
    elif add_type == 'add_pcg':
        tDn = 'topology/pod-%s/paths-%s/pathep-[%s]' % (pod, node_id, port)
    elif add_type == 'add_vpc':
        x = node_id.split(',')
        node_1 = x[0]
        node_2 = x[1]
        tDn = 'topology/pod-%s/protpaths-%s-%s/pathep-[%s]' % (pod, node_1, node_2, port)

    afile.write('resource "aci_epg_to_static_path" "%s_%s_%s" {\n' % (switch_ipr, int_select, epg))
    afile.write('\tdepends_on           = [aci_application_epg.%s,aci_ranges.st_vlan_pool_add_%s]\n' % (epg, vlan))
    afile.write('\tapplication_epg_dn   = aci_application_epg.%s.id\n' % (epg))
    afile.write('\ttdn                  = "%s"\n' % (tDn))
    afile.write('\tencap                = "vlan-%s"\n' % (vlan))
    afile.write('\tmode                 = "%s"\n' % (vl_mode))
    afile.write('}\n\n')
    
def resource_bds(add_type, tenant, vrf, bd_name, extend, enforcement, descr):
    arpflood = '%s' % (extend)
    if extend == 'yes':
        optimiz_w = 'no'
        mdest = 'bd-flood'
        unkmac = 'flood'
        unkmcast = 'flood'
    else:
        optimiz_w = 'yes'
        mdest = 'bd-flood'
        unkmac = 'proxy'
        unkmcast = 'opt-flood'
    wr_file = wr_bds
    wr_file.write('resource "aci_bridge_domain" "%s" {\n' % (bd_name))
    wr_file.write('\tdepends_on                  = [aci_vrf.%s]\n' % (vrf))
    wr_file.write('\ttenant_dn                   = aci_tenant.%s.id\n' % (tenant))
    wr_file.write('\tdescription                 = "%s bridge domain"\n' % (bd_name))
    wr_file.write('\tname                        = "%s"\n' % (bd_name))
    wr_file.write('\toptimize_wan_bandwidth      = "%s"\n' % (optimiz_w))
    wr_file.write('\tarp_flood                   = "%s"\n' % (arpflood))
    wr_file.write('\tep_move_detect_mode         = "garp"\n')
    wr_file.write('\tip_learning                 = "yes"\n')
    wr_file.write('\tipv6_mcast_allow            = "no"\n')
    wr_file.write('\tlimit_ip_learn_to_subnets   = "yes"\n')
    wr_file.write('\tmcast_allow                 = "yes"\n')
    wr_file.write('\tmulti_dst_pkt_act           = "%s"\n' % (mdest))
    wr_file.write('\tbridge_domain_type          = "regular"\n')
    wr_file.write('\tunk_mac_ucast_act           = "%s"\n' % (unkmac))
    wr_file.write('\tunk_mcast_act               = "%s"\n' % (unkmcast))
    wr_file.write('\trelation_fv_rs_ctx          = aci_vrf.%s.id\n' % (vrf))
    wr_file.write('}\n\n')

    if add_type == 'nca_bd':
        wr_file = wr_epgs
        name = bd_name.split('_')
        epg = '%s_epg' % (name[0])
        net_centric_epg(tenant, bd_name, epg, enforcement, descr, wr_file)

def resource_epgs(add_type, tenant, bd_name, epg_name, enforcement, descr):
    if add_type == 'nca_epg':
        wr_file = wr_epgs
        net_centric_epg(tenant, bd_name, epg_name, enforcement, descr, wr_file)

def resource_pgs_access(add_type, switch_ipr, int_select, node_id, pg_name, aep, mtu, speed, swpt_mode, acc_vlan, trunk_vlans, cdp, lldp, bpdu, descr):

    try:
        # Validate User Inputs
        # validating.name_rule(line_count, vrf_name)
        validating.node_id(line_count, node_id)
    except Exception as err:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}.  Please verify input information.  Exiting....')
        print(f'\n-----------------------------------------------------------------------------\n')
        exit()
    
    # Build Template and Populate Template
    wr_file = wr_portgps

    pg_regex = re.compile('(2x100g_pg|4x100g_pg|4x10g_pg|4x25g_pg|8x50g_pg|access_host_apg|inband_apg)')
    pg_count = 0
    if re.search(pg_regex, pg_name):
        pg_count =+ 1
    else:
        wr_file.seek(0) # Read the file from the beginning
        if pg_name in wr_file.read():
            pg_count =+ 1
        bpdu
    if pg_count == 0:
        wr_file.write('resource "aci_leaf_access_port_policy_group" "%s" {\n' % (pg_name))
        wr_file.write('\tdescription 				       = "%s"\n' % (descr))
        wr_file.write('\tname 						       = "%s"\n' % (pg_name))
        wr_file.write('\trelation_infra_rs_att_ent_p	       = "uni/infra/attentp-%s"\n' % (aep))
        wr_file.write('\trelation_infra_rs_cdp_if_pol       = "uni/infra/cdpIfP-%s"\n' % (cdp))
        wr_file.write('\trelation_infra_rs_h_if_pol	       = "uni/infra/hintfpol-%s"\n' % (speed))
        wr_file.write('\trelation_infra_rs_lldp_if_pol      = "uni/infra/lldpIfP-%s"\n' % (lldp))
        wr_file.write('\trelation_infra_rs_mcp_if_pol       = "uni/infra/mcpIfP-mcp_Enabled"\n')
        wr_file.write('\trelation_infra_rs_mon_if_infra_pol = "uni/infra/moninfra-default"\n')
        if not bpdu == '':
            wr_file.write('\trelation_infra_rs_stp_if_pol       = "uni/infra/ifPol-%s"\n' % (bpdu))
        wr_file.write('}\n\n')
    
    wr_file.seek(0) # Read the file from the beginning
    pg_str = '%s_%s_pg' % (switch_ipr, int_select)
    if not pg_str in wr_file.read():
        rtDn = 'accportgrp-%s' % (pg_name)
        pg_to_int_select(switch_ipr, int_select, rtDn, wr_file)

    # Add Description to Interface Selector for Policy Group if Needed
    # assign_int_descr(switch_ipr, int_select, wr_file)

    # Need to modify the port name from Eth1-1 to eth1/1 in example
    port = convert_selector_to_port(int_select)

    # Define File for adding static Path Binding and Open for Appending resources
    file_stbind = './fabric/resources_user_static_bindings_%s.tf' % (switch_ipr)
    afile = open(file_stbind, 'a+')

    # Add Access VLAN or Native VLAN for Trunk
    vlan = acc_vlan
    vl_mode = 'native'
    netcentric = aci.function_vlan_to_netcentric(vlan)
    epg = '%s_epg' % (netcentric)
    add_epg_and_vlan(add_type, pod, switch_ipr, node_id, int_select, port, epg, vlan, vl_mode, afile)

    # If this is a Trunk Port do the Static Bindings for All the EPGs
    if swpt_mode == 'trunk':
        vlan_list = aci.vlan_list_full(trunk_vlans)
        for v in vlan_list:
            vlan = v
            vl_mode = 'regular'
            netcentric = aci.function_vlan_to_netcentric(vlan)
            epg = '%s_epg' % (netcentric)
            add_epg_and_vlan(add_type, pod, switch_ipr, node_id, int_select, port, epg, vlan, vl_mode, afile)

    
    afile.close()

def resource_pgs_brkout(int_select, switch_role, module, model, node_id, switch_ipr, pod, brkout_pg, descr):

    try:
        # Validate User Inputs
        # validating.name_rule(line_count, vrf_name)
        validating.node_id(line_count, node_id)
    except Exception as err:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}.  Please verify input information.  Exiting....')
        print(f'\n-----------------------------------------------------------------------------\n')
        exit()
    
    # Build Template and Populate Template
    wr_file = wr_portgps

    # If Needed Add Breakout Port Group to Interface Selector
    wr_file.seek(0) # Read the file from the beginning
    pg_str = '%s_%s_pg' % (switch_ipr, int_select)
    if not pg_str in wr_file.read():
        rtDn = 'brkoutportgrp-%s' % (brkout_pg)
        pg_to_int_select(switch_ipr, int_select, rtDn, wr_file)

    brk_split = brkout_pg.split('x')
    brk_count = int(brk_split[0])
    loop_count = 1
    while loop_count <= brk_count:
        brkout_select = int_select + '-' + str(loop_count)
        xa = int_select.replace('Eth', 'eth')
        xa = xa.replace('-', '/')
        xb = xa.split('/')
        subport = loop_count
        if re.search('^00', xb[1]):
            xc = xb[1].replace('00', '', 1)
            #interf = '%s/%s/%s' % (xb[0], xc, loop_count)
            port = xc
        elif re.search('^0', xb[1]):
            xc = xb[1].replace('0', '', 1)
            #interf = '%s/%s/%s' % (xb[0], xc, loop_count)
            port = xc
        else:
            #interf = xa
            port = xb[1]
        search_string = '%s_%s' % (switch_ipr, brkout_select)
        wr_file.seek(0)
        if not search_string in wr_file.read():
            if switch_role == 'leaf':
                wr_file.write('resource "aci_access_port_selector" "%s_%s" {\n' % (switch_ipr, brkout_select))
                wr_file.write('\tleaf_interface_profile_dn  = aci_leaf_interface_profile.%s.id\n' % (switch_ipr))
                wr_file.write('\tdescription                = "%s"\n' % (descr))
                wr_file.write('\tname                       = "%s"\n' % (brkout_select))
                wr_file.write('\taccess_port_selector_type  = "range"\n')
                wr_file.write('}\n\n')

                wr_file.write('resource "aci_access_sub_port_block" "%s_%s" {\n' % (switch_ipr, brkout_select))
                wr_file.write('\tdepends_on                 = [aci_leaf_interface_profile.%s]\n' % (switch_ipr))
                wr_file.write('\taccess_port_selector_dn    = aci_access_port_selector.%s_%s.id\n' % (switch_ipr, brkout_select))
                wr_file.write('\tname                       = "block2"\n')
                wr_file.write('\tfrom_card                  = "%s"\n' % (module))
                wr_file.write('\tfrom_port                  = "%s"\n' % (port))
                wr_file.write('\tfrom_sub_port              = "%s"\n' % (subport))
                wr_file.write('\tto_card                    = "%s"\n' % (module))
                wr_file.write('\tto_port                    = "%s"\n' % (port))
                wr_file.write('\tto_sub_port                = "%s"\n' % (subport))
                wr_file.write('}\n\n')
        loop_count += 1

def resource_pgs_bundle(add_type, switch_ipr, int_select, node_id, pg_name, aep, lacp, mtu, speed, swpt_mode, acc_vlan, trunk_vlans, cdp, lldp, bpdu, pc_descr, descr):
    if add_type == 'add_vpc':
        x = node_id.split(',')
        node_1 = x[0]
        node_2 = x[1]
    try:
        # Validate User Inputs
        # validating.name_rule(line_count, vrf_name)
        if add_type == 'add_vpc':
            validating.node_id(line_count, node_1)
            validating.node_id(line_count, node_2)
        else:
            validating.node_id(line_count, node_id)
    except Exception as err:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}.  Please verify input information.  Exiting....')
        print(f'\n-----------------------------------------------------------------------------\n')
        exit()
    
    # Build Template and Populate Template
    wr_file = wr_portgps

    pg_regex = re.compile('(2x100g_pg|4x100g_pg|4x10g_pg|4x25g_pg|8x50g_pg|access_host_apg|inband_apg)')
    pg_count = 0
    if re.search(pg_regex, pg_name):
        pg_count =+ 1
    else:
        wr_file.seek(0) # Read the file from the beginning
        if pg_name in wr_file.read():
            pg_count =+ 1
    if pg_count == 0:
        wr_file.write('resource "aci_leaf_access_bundle_policy_group" "%s" {\n' % (pg_name))
        wr_file.write('\tdescription 				       = "%s"\n' % (pc_descr))
        wr_file.write('\tname 						       = "%s"\n' % (pg_name))
        wr_file.write('\tlag_t 						       = "%s"\n' % (lag_type))
        wr_file.write('\trelation_infra_rs_att_ent_p	       = "uni/infra/attentp-%s"\n' % (aep))
        wr_file.write('\trelation_infra_rs_cdp_if_pol       = "uni/infra/cdpIfP-%s"\n' % (cdp))
        wr_file.write('\trelation_infra_rs_h_if_pol	       = "uni/infra/hintfpol-%s"\n' % (speed))
        wr_file.write('\trelation_infra_rs_lacp_pol         = "uni/infra/lacplagp-%s"\n' % (lacp))
        wr_file.write('\trelation_infra_rs_lldp_if_pol      = "uni/infra/lldpIfP-%s"\n' % (lldp))
        wr_file.write('\trelation_infra_rs_mcp_if_pol       = "uni/infra/mcpIfP-mcp_Enabled"\n')
        wr_file.write('\trelation_infra_rs_mon_if_infra_pol = "uni/infra/moninfra-default"\n')
        if not bpdu == '':
            wr_file.write('\trelation_infra_rs_stp_if_pol       = "uni/infra/ifPol-%s"\n' % (bpdu))
        wr_file.write('}\n\n')
    
    wr_file.seek(0) # Read the file from the beginning
    pg_str = '%s_%s_pg' % (switch_ipr, int_select)
    if not pg_str in wr_file.read():
        rtDn = 'accbundle-%s' % (pg_name)
        pg_to_int_select(switch_ipr, int_select, rtDn, wr_file)

    # Add Description to Interface Selector for Policy Group if Needed
    # assign_int_descr(switch_ipr, int_select, wr_file)

    # Define File for adding static Path Binding and Open for Appending resources
    file_stbind = './fabric/resources_user_static_bindings_%s.tf' % (switch_ipr)
    afile = open(file_stbind, 'a+')

    # Add Access VLAN or Native VLAN for Trunk
    port = pg_name
    vlan = acc_vlan
    vl_mode = 'native'
    netcentric = aci.function_vlan_to_netcentric(vlan)
    epg = '%s_epg' % (netcentric)
    add_epg_and_vlan(add_type, pod, switch_ipr, node_id, int_select, port, epg, vlan, vl_mode, afile)

    # If this is a Trunk Port do the Static Bindings for All the EPGs
    if swpt_mode == 'trunk':
        vlan_list = aci.vlan_list_full(trunk_vlans)
        for v in vlan_list:
            vlan = v
            vl_mode = 'regular'
            netcentric = aci.function_vlan_to_netcentric(vlan)
            epg = '%s_epg' % (netcentric)
            add_epg_and_vlan(add_type, pod, switch_ipr, node_id, int_select, port, epg, vlan, vl_mode, afile)
    
    afile.close()

def resource_tenant(tenant_name, tenant_descr):
    try:
        # Validate Tenant Name
        validating.name_rule(line_count, tenant_name)
    except Exception as err:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}.  Please verify input information.  Exiting....')
        print(f'\n-----------------------------------------------------------------------------\n')
        exit()
    
    # Build Template and Populate Template
    wr_file = wr_tenants
    wr_file.write('resource "aci_tenant" "%s" {\n' % (tenant_name))
    wr_file.write('\tdescription    = "%s"\n' % (tenant_descr))
    wr_file.write('\tname           = "%s"\n' % (tenant_name))
    wr_file.write('}\n\n')

    wr_file = wr_apps
    wr_file.write('resource "aci_application_profile" "%s_nets" {\n' % (tenant_name))
    wr_file.write('\tdepends_on = [aci_tenant.%s]\n' % (tenant_name))
    wr_file.write('\ttenant_dn  = aci_tenant.%s.id\n' % (tenant_name))
    wr_file.write('\tname       = "nets"\n')
    #wr_file.write('\tprio       = "level1"\n')
    wr_file.write('}\n\n')

def resource_vrf(tenant_name, vrf_name, vrf_desc, fltr_type):
    try:
        # Validate Tenant and VRF Name
        validating.name_rule(line_count, tenant_name)
        validating.name_rule(line_count, vrf_name)
    except Exception as err:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}.  Please verify input information.  Exiting....')
        print(f'\n-----------------------------------------------------------------------------\n')
        exit()
    
    # Build Template and Populate Template
    wr_file = wr_vrfs

    # Add VRF to Resource File
    wr_file.write('resource "aci_vrf" "%s" {\n' % (vrf_name))
    wr_file.write('\ttenant_dn                           = "uni/tn-%s"\n' % (tenant_name))
    wr_file.write('\tname                                = "%s"\n' % (vrf_name))
    wr_file.write('\tbd_enforced_enable                  = "yes"\n')
    wr_file.write('\tip_data_plane_learning			    = "enabled"\n')
    wr_file.write('\tpc_enf_pref						    = "enforced"\n')
    wr_file.write('\tpc_enf_dir						    = "ingress"\n')
    wr_file.write('\trelation_fv_rs_ctx_mon_pol		    = "uni/tn-common/monepg-default"\n')
    wr_file.write('\trelation_fv_rs_ctx_to_ep_ret		= "uni/tn-common/epRPol-default"\n')
    wr_file.write('\trelation_fv_rs_vrf_validation_pol   = "uni/tn-common/vrfvalidationpol-default"\n')
    wr_file.write('}\n\n')

    wr_file.write('resource "aci_any" "%s_any" {\n' % (vrf_name))
    wr_file.write('\tdepends_on                     = [aci_vrf.%s]\n' % (vrf_name))
    wr_file.write('\tvrf_dn                         = "uni/tn-%s/ctx-%s"\n' % (tenant_name, vrf_name))
    wr_file.write('\tdescription                    = "%s"\n' % (vrf_desc))

    if fltr_type == 'pg':
        wr_file.write('\tpref_gr_memb  				   = "enabled"\n')
        wr_file.write('}\n\n')
    elif fltr_type == 'vzAny':
        wr_file.write('\tmatch_t      				   = "AtleastOne"\n')
        #wr_file.write('\trelation_vz_rs_any_to_cons = [data.aci_contract.default.id]\n')
        #wr_file.write('\trelation_vz_rs_any_to_prov	= [data.aci_contract.default.id]\n')
        wr_file.write('}\n\n')

        # Define Variables for Template Creation - vzAny Contracts
        # Tenants > Networking > VRFs > {VRF Name} > EPG Collection for VRF: Provider/Consumer Contracts
        path_attrs = '/api/node/mo/uni/tn-%s/ctx-%s/any.json' % (tenant_name, vrf_name)
        class_name_1 = 'vzRsAnyToCons'
        class_name_2 = 'vzRsAnyToProv'

        # Format Variables for JSON Output
        data_out_1 = {class_name_1: {'attributes': {'tnVzBrCPName': 'default'}}}
        data_out_2 = {class_name_2: {'attributes': {'tnVzBrCPName': 'default'}}}

        # Write Output to Resource Files using Template
        resrc_desc = 'vzAny_%s_Cons' % (vrf_name)
        tf_templates.aci_rest(resrc_desc, path_attrs, class_name_1, data_out_1, wr_file)
        resrc_desc = 'vzAny_%s_Prov' % (vrf_name)
        tf_templates.aci_rest(resrc_desc, path_attrs, class_name_2, data_out_2, wr_file)

def st_vlan_pool(vlan, wr_file):
    wr_file.write('resource "aci_ranges" "st_vlan_pool_add_%s" {\n' % (vlan))
    wr_file.write('\tvlan_pool_dn   = "uni/infra/vlanns-[access_vl-pool]-static"\n')
    wr_file.write('\t_from          = "vlan-%s"\n' % (vlan))
    wr_file.write('\tto		       = "vlan-%s"\n' % (vlan))
    wr_file.write('}\n\n')

line_count = 1
# Loop Through User Defined Tenants in Worksheet "Tenant"
for r in ws1.rows:
    if any(r):
        type = str(r[0].value)
        if type == 'tnt_add':
            tenant_name = str(r[1].value)
            tenant_desc = str(r[2].value)

            # Create Resource Records for Tenant
            resource_tenant(tenant_name, tenant_desc)
            line_count += 1
        elif type == 'tnt_vrf':
            tenant_name = str(r[1].value)
            tenant_desc = str(r[2].value)
            vrf_name = '%s_vrf' % (tenant_name)
            vrf_desc = str(r[5].value)
            fltr_type = str(r[8].value)

            # Create Resource Records for Tenant and VRF
            resource_tenant(tenant_name, tenant_desc)
            tnt_name = 'common'
            resource_vrf(tnt_name, vrf_name, vrf_desc, fltr_type)
            line_count += 1
        else:
            line_count += 1
    else:
        line_count += 1

line_count = 1
# Loop Through User Defined VRFs in Worksheet "VRF"
for r in ws2.rows:
    if any(r):        
        type = str(r[0].value)
        if type == 'vrf_add':
            tenant_name = str(r[1].value)
            vrf_name = str(r[2].value)
            vrf_desc = str(r[3].value)
            fltr_type = str(r[6].value)

            # Create Resource Records for VRF
            resource_vrf(tnt_name, vrf_name, vrf_desc, fltr_type)
            line_count += 1
        else:
            line_count += 1
    else:
        line_count += 1

line_count = 1
# Loop Through User Defined L3Outs in Worksheet "L3Out"
for r in ws3.rows:
    if any(r):        
        type = str(r[0].value)
        if type == 'l3out':
            l3_host_tnt = str(r[1].value)
            l3out_tenant = str(r[2].value)
            l3_domain = str(r[3].value)
            routing_pt = str(r[4].value)
            intf_type = str(r[5].value)

            # Create Resource Records for VRF
            #resource_vrf(tnt_name, vrf_name, vrf_desc, fltr_type)
            line_count += 1
        else:
            line_count += 1
    else:
        line_count += 1

line_count = 1
# Loop Through User Defined Tenants in Worksheet "Bridge Domain"
for r in ws4.rows:
    if any(r):
        type = str(r[0].value)
        if type == 'add_bd' or type == 'nca_bd':
            add_type = str(r[0].value)
            tenant = str(r[1].value)
            vrf = str(r[2].value)
            bd_name = str(r[3].value)
            extend = str(r[4].value)
            enforcement = str(r[4].value)
            descr = str(r[6].value)

            # Create Resource Records for Bridge Domains and Possibly EPGs
            resource_bds(add_type, tenant, vrf, bd_name, extend, enforcement, descr)
            line_count += 1
        else:
            line_count += 1
    else:
        line_count += 1

line_count = 1
# Loop Through User Defined Tenants in Worksheet "App and EPG"
for r in ws7.rows:
    if any(r):
        type = str(r[0].value)
        if type == 'add_epg' or type == 'nca_epg':
            add_type = str(r[0].value)
            tenant = str(r[1].value)
            epg_name = str(r[3].value)
            bd_name = str(r[7].value)
            enforcement = str(r[4].value)
            descr = str(r[6].value)

            # Create Resource Records for Bridge Domains and Possibly EPGs
            #resource_epgs(add_type, tenant, epg_name, enforcement, descr)
            line_count += 1
        else:
            line_count += 1
    else:
        line_count += 1

line_count = 1
# Loop Through User Defined Tenants in Worksheet "Tenant"
for r in ws8.rows:
    if any(r):
        type = str(r[0].value)
        if type == 'add_apg' or type == 'add_pcg' or type == 'add_vpc':
            switch_ipr = str(r[1].value)
            int_select = str(r[2].value)
            node_id = str(r[3].value)
            pg_name = str(r[4].value)
            aep = str(r[5].value)
            lacp = str(r[6].value)
            pod = str(r[7].value)
            mtu = str(r[8].value)
            speed = str(r[9].value)
            swpt_mode = str(r[10].value)
            acc_vlan = str(r[11].value)
            trunk_vlans = str(r[12].value)
            cdp = str(r[13].value)
            lldp = str(r[14].value)
            bpdu = str(r[16].value)
            pc_descr = str(r[17].value)
            descr = str(r[18].value)
            if cdp == 'no':
                cdp = 'cdp_Disabled'
            else:
                cdp = 'cdp_Enabled'
            if lldp == 'no':
                lldp = 'lldp_Disabled'
            else:
                lldp = 'lldp_Enabled'
            if bpdu == 'yes':
                bpdu = 'BPDU_fg'
            elif bpdu == 'no':
                bpdu = ''
            if type == 'add_pcg':
                lag_type = 'node'
            elif type == 'add_vpc':
                lag_type = 'link'

            # Create Resource Records for Port Groups
            add_type = type
            if type == 'add_apg':
                resource_pgs_access(add_type, switch_ipr, int_select, node_id, pg_name, aep, mtu, speed, swpt_mode, acc_vlan, 
                                    trunk_vlans, cdp, lldp, bpdu, descr)
            elif type == 'add_pcg' or type == 'add_vpc':
                resource_pgs_bundle(add_type, switch_ipr, int_select, node_id, pg_name, aep, lacp, mtu, speed, swpt_mode, acc_vlan, 
                                    trunk_vlans, cdp, lldp, bpdu, pc_descr, descr)
            line_count += 1
        elif type == 'brk_out':
            int_selector = str(r[1].value)
            switch_role = str(r[2].value)
            module = str(r[3].value)
            model = str(r[4].value)
            node_id = str(r[5].value)
            switch_ipr = str(r[6].value)
            pod = str(r[7].value)
            brkout_pg = str(r[8].value)
            descr = str(r[12].value)
 
             # Create Resource Records for Port Groups
            resource_pgs_brkout(int_selector, switch_role, module, model, node_id, switch_ipr, pod, brkout_pg, descr)
            line_count += 1
        else:
            line_count += 1
    else:
        line_count += 1

# Close out the Open Files
#csv_file.close()
wr_apps.close()
wr_epgs.close()
wr_bds.close()
wr_portgps.close()
wr_tenants.close()
wr_vrfs.close()
wr_vlans.close()


#End Script
print(f'\n-----------------------------------------------------------------------------\n')
print(f'   Completed Running Script.  Exiting....')
print(f'\n-----------------------------------------------------------------------------\n')
exit()