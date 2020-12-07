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
ws3 = wb['BD, App, EPG']
ws4 = wb['Subnet']
ws5 = wb['L3Out']
ws6 = wb['DHCP Relay']
ws7 = wb['Access Interfaces']
ws8 = wb['Static Port Mappings']

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
file_tfstate = './fabric/terraform.tfstate'
file_vrfs = './fabric/resources_user_input_VRFs.tf'
file_vlans = './fabric/resources_user_input_VLANs.tf'
read_tfstate = open(file_tfstate, 'r')
wr_apps = open(file_apps, 'w+')
wr_epgs = open(file_epgs, 'w+')
wr_bds = open(file_bds, 'w+')
wr_portgps = open(file_portgps, 'w+')
wr_tenants = open(file_tenants, 'w+')
wr_vrfs = open(file_vrfs, 'w+')
wr_vlans = open(file_vlans, 'w+')
#wr_apps.write('# This File will include Applications\n\nvariable \"user_apps\" {\n\tdefault = {\n')
wr_apps.write('# This File will include Applications\n\n')
wr_epgs.write('# This File will include EPGs\n\n')
wr_bds.write('# This File will include Bridge Domains\n\n')
wr_portgps.write('# This File will include Port Group Confgiuration and Mapping\n\n')
wr_tenants.write("# This File will include Tenants\n\n")
wr_vrfs.write("# This File will include VRFs\n\n")

pg_regex = re.compile('(2x100g_pg|4x100g_pg|4x10g_pg|4x25g_pg|8x50g_pg|access_host_apg|inband_apg)')

# Add Data source for Default Tenants
default_tenants = ['common', 'infra', 'mgmt']
for tnt in default_tenants:
    wr_tenants.write('data "aci_tenant" "%s" {' % (tnt))
    wr_tenants.write('\tname    = "%s"' % (tnt))
    wr_tenants.write('}\n\n')

def apic_login():
    APICIP = None
    APICUSER = None
    APICPASS = None
    APICIP = 'brahma-apic2.rich.ciscolabs.com'
    APICUSER = 'admin'
    APICPASS = 'cisco123'
    
    # Disable urllib3 warnings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # Prompt for APIC IP if the constant is None
    if APICIP is not None:
        apic = APICIP
    else:
        while True:
            apic = input('Enter the APIC IP: ')
            try:
                ipaddress.ip_address(apic)
                break
            except Exception as e:
                print('Enter a valid IP address. Error received: {}'.format(e))
    
    # Prompt for APIC Username if the constant is None
    if APICUSER is not None:
        user = APICUSER
    else:
        user = input('Enter APIC username: ')
    
    # Prompt for APIC Password if the constant is None
    if APICPASS is not None:
        pword = APICPASS
    else:
        while True:
            try:
                pword = getpass.getpass(prompt='Enter APIC password: ')
                break
            except Exception as e:
                print('Something went wrong. Error received: {}'.format(e))
    
    # Initialize the fabric login method, passing appropriate variables
    fablogin = aci.FabLogin(apic, user, pword)
    # Run the login and load the cookies var
    cookies = fablogin.login()

    # Placeholder
    if cookies == 'xyz':
        print('yummy')

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
    if '_' in xa:
        xa = xa.replace('_', '/')
    if '-' in xa:
        xa = xa.replace('-', '/')
    xb = xa.split('/')
    xcount = len(xb)
    if xcount == 3:
        if re.search('^0', xb[2]):
            xc = xb[2].replace('00', '', 1)
            port = '%s/%s/%s' % (xb[0], xb[1], xc)
        else:
            port = xa
    elif xcount == 2:
        if re.search('^0', xb[1]):
            xc = xb[1].replace('00', '', 1)
            port = '%s/%s' % (xb[0], xc)
        else:
            port = xa
    return port

def loop_static_path_vlan_lists(line_count, add_type, pod, switch_ipr, node_id, pg_name, swpt_mode, native_vlan, trunk_vlans):
    # Need to get VLAN to EPG Mapping from "BD, App, EPG" Worksheet for Native VLAN
    if not native_vlan == '':
        vlan = native_vlan
        vl_mode = 'native'
        tenant,app,epg = vlan_to_epg_mapping(line_count,vlan)
        if tenant == '' or app == '' or epg == '':
            validating.error_vlan_to_epg(line_count, vlan, ws3)
        else:
            resource_static_path(line_count, add_type, pod, switch_ipr, node_id, pg_name, tenant, app, epg, vlan, vl_mode)

            # Add VLAN to STatic VLAN Pool if it Doesn't Exist
            wr_file = wr_vlans
            wr_file.seek(0)
            vlan_descr = 'st_vlan_pool_add_%s' % (vlan)
            if not vlan_descr in wr_file.read():
                resource_static_vlan_pool(vlan, wr_file)

    # If this is a Trunk Port get VLAN to EPG Mapping from "BD, App, EPG"
    # If Exists then create Static Paths
    if swpt_mode == 'trunk':
        vlan_list = aci.vlan_list_full(trunk_vlans)
        for v in vlan_list:
            vlan = (v)
            vl_mode = 'regular'
            tenant,app,epg = vlan_to_epg_mapping(line_count,vlan)
            if not tenant == '' and not app == '' and not epg == '':
                resource_static_path(line_count, add_type, pod, switch_ipr, node_id, pg_name, tenant, app, epg, vlan, vl_mode)

                # Add VLAN to STatic VLAN Pool if it Doesn't Exist
                wr_file = wr_vlans
                wr_file.seek(0)
                vlan_descr = 'st_vlan_pool_add_%s' % (vlan)
                if not vlan_descr in wr_file.read():
                    resource_static_vlan_pool(vlan, wr_file)
    
def resource_app(tenant, app, priority):
    # Add Application Profile to App Resource File
    wr_file = wr_apps
    wr_file.write('resource "aci_application_profile" "%s_%s" {\n' % (tenant, app))
    wr_file.write('\tdepends_on = [aci_tenant.%s]\n' % (tenant))
    wr_file.write('\ttenant_dn  = aci_tenant.%s.id\n' % (tenant))
    wr_file.write('\tname       = "%s"\n' % (app))
    wr_file.write('\tprio       = "%s"\n' % (priority))
    wr_file.write('}\n\n')

def resource_bds(tenant, bd, bd_descr, extend, vrf):
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
    wr_file.write('resource "aci_bridge_domain" "%s" {\n' % (bd))
    wr_file.write('\tdepends_on                  = [aci_vrf.%s]\n' % (vrf))
    wr_file.write('\ttenant_dn                   = aci_tenant.%s.id\n' % (tenant))
    wr_file.write('\tdescription                 = "%s"\n' % (bd_descr))
    wr_file.write('\tname                        = "%s"\n' % (bd))
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

def resource_domain_to_epg(tenant, app, epg, domain, wr_file):
    # Define Variables for Template Creation - Domain to EPG
    # {Tenant} > Application Profiles > {Application Name} > Application EPGs > {EPG Name} > Domains (VMs and Bare-Metals): Add Domain
    resrc_desc = '%s_to_%s' % (domain, epg)
    depends_on = 'aci_application_epg.%s_%s_%s' % (tenant, app, epg)
    class_name = 'fvRsDomAtt'
    tDn_string = 'uni/%s' % (domain)
    path_attrs = '/api/node/mo/uni/tn-%s/ap-%s/epg-%s.json' % (tenant, app, epg)

    # Format Variables for JSON Output
    data_out = {class_name: {'attributes': {'tDn': tDn_string}, 'children': []}}

    # Write Output to Resource Files using Template
    tf_templates.aci_rest_depends_on(resrc_desc, depends_on, path_attrs, class_name, data_out, wr_file)

def resource_epg(tenant, bd, app, epg, priority, qos_policy, enforcement, enf_type, epg_descr, shut_down):

    if enf_type == 'preferred_group':
        pref_grp = 'include'
    else:
        pref_grp = 'exclude'
    if shut_down == '':
        shut_down = 'no'

    wr_file = wr_epgs
    wr_file.write('resource "aci_application_epg" "%s_%s_%s" {\n' % (tenant, app, epg))
    wr_file.write('\tdepends_on                     = [aci_application_profile.%s_%s]\n' % (tenant, app))
    wr_file.write('\tapplication_profile_dn         = aci_application_profile.%s_%s.id\n' % (tenant, app))
    wr_file.write('\tname                           = "%s"\n' % (epg))
    wr_file.write('\tdescription                    = "%s"\n' % (epg_descr))
    wr_file.write('\tflood_on_encap                 = "disabled"\n')
    wr_file.write('\thas_mcast_source               = "no"\n')
    wr_file.write('\tis_attr_based_epg              = "no"\n')
    wr_file.write('\tmatch_t                        = "AtleastOne"\n')
    wr_file.write('\tpc_enf_pref                    = "%s"\n' % (enforcement))
    wr_file.write('\tpref_gr_memb                   = "%s"\n' % (pref_grp))
    wr_file.write('\tprio                           = "%s"\n' % (priority))
    wr_file.write('\tshutdown                       = "%s"\n' % (shut_down))
    wr_file.write('\trelation_fv_rs_bd              = aci_bridge_domain.%s.id\n' % (bd))
    wr_file.write('\trelation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"\n')
    if not qos_policy == 'None':
        wr_file.write('\trelation_fv_rs_cust_qos_pol    = "%s"\n' % (qos_policy))
    wr_file.write('}\n\n')

    # Assign Physical domain to EPG
    domain = 'phys-access_phys'
    resource_domain_to_epg(tenant, app, epg, domain, wr_file)

def resource_pg_to_int_select(switch_ipr, int_select, rtDn, wr_file):
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

def resource_pgs_access(add_type, switch_ipr, int_select, pg_name, aep, mtu, speed, cdp, lldp, bpdu, descr):

    # Build Template and Populate Template
    wr_file = wr_portgps

    # Check if Interface Policy Group Exists and if Not Create it
    pg_count = 0
    if re.search(pg_regex, pg_name):
        pg_count =+ 1
    else:
        rsc_pg = '"aci_leaf_access_port_policy_group" "%s"' % (pg_name)
        wr_file.seek(0) # Read the file from the beginning
        if rsc_pg in wr_portgps.read():
            pg_count =+ 1
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
    
    wr_file.seek(0)
    pg_str = '%s_%s_pg' % (switch_ipr, int_select)
    if not pg_str in wr_file.read():
        rtDn = 'accportgrp-%s' % (pg_name)
        resource_pg_to_int_select(switch_ipr, int_select, rtDn, wr_file)

        # Add Description to Interface Selector for Policy Group if Needed
        # assign_int_descr(switch_ipr, int_select, wr_file)

def resource_pgs_brkout(switch_ipr, int_select, switch_role, model, module, brkout_pg, descr):

    try:
        # Validate User Inputs
        # validating.name_rule(line_count, vrf_name)
        validating.brkout_pg(line_count, brkout_pg)
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
        resource_pg_to_int_select(switch_ipr, int_select, rtDn, wr_file)

    brk_split = brkout_pg.split('x')
    brk_count = int(brk_split[0])
    loop_count = 1
    while loop_count <= brk_count:
        brkout_select = int_select + '-' + str(loop_count)
        xa = int_select.replace('Eth', 'eth')
        if '_' in xa:
            xa = xa.replace('_', '/')
        if '-' in xa:
            xa = xa.replace('-', '/')
        xb = xa.split('/')
        subport = loop_count
        if re.search('^0', xb[1]):
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

def resource_pgs_bundle(add_type, switch_ipr_1, int_select, aep, pg_name, lacp, mtu, speed, cdp, lldp, bpdu, pc_descr, descr):
    # Check if Interface Policy Group Exists and if Not Create it
    wr_portgps.seek(0)

    # Build Template and Populate Template
    wr_file = wr_portgps

    pg_count = 0
    rsc_pg = '"aci_leaf_access_bundle_policy_group" "%s"' % (pg_name)
    if rsc_pg in wr_file.read():
        pg_count =+ 1

    # If Interface Policy Group Doesn't Exist Create it
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
        resource_pg_to_int_select(switch_ipr, int_select, rtDn, wr_file)

    # Add Description to Interface Selector for Policy Group if Needed
    # assign_int_descr(switch_ipr, int_select, wr_file)

def resource_static_path(line_count, add_type, pod, switch_ipr, node_id, pg_name, tenant, app, epg, vlan, vl_mode):
    if add_type == 'static_vpc':
        if not ',' in node_id:
            print(f'\n-----------------------------------------------------------------------------\n')
            print(f'   Error on Row {line_count} of {ws8}.  There should be ')
            print(f'   two nodes; comma seperatred for static_vpc type.  Exiting....')
            print(f'\n-----------------------------------------------------------------------------\n')
            exit()

        x = node_id.split(',')
        node_1 = x[0]
        node_2 = x[1]
        y = switch_ipr.split(',')
        switch_ipr = y[0]
    try:
        # Validate User Inputs
        if add_type == 'static_vpc':
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

        if add_type == 'static_vpc':
            xz = switch_ipr.split(',')
            sw1 = xz[0]
            sw2 = xz[1]
            if not '{}_count'.format(sw1) in locals():
                x = '{}_count'.format(sw1)
                x = 0
            if '{}_count'.format(sw1) == 0:
                x += 1
                delete_file = 'rm ./fabric/resources_user_static_bindings_%s.tf' % (sw1)
                os.system(delete_file)
        else:
            if not '{}_count'.format(switch_ipr) in locals():
                x = '{}_count'.format(switch_ipr)
                x = 0
            if '{}_count'.format(switch_ipr) == 0:
                x += 1
                delete_file = 'rm ./fabric/resources_user_static_bindings_%s.tf' % (switch_ipr)
                os.system(delete_file)



    # Create tDn attribute based on Type of Port being Configured
    if add_type == 'static_apg':
        # Need to modify the port name from Eth1-1 to eth1/1 in example
        pg_name_1 = pg_name
        pg_name = convert_selector_to_port(pg_name)
        tDn = 'topology/pod-%s/paths-%s/pathep-[%s]' % (pod, node_id, pg_name)
        pg_name = pg_name_1
    elif 'pcg' in add_type:
        tDn = 'topology/pod-%s/paths-%s/pathep-[%s]' % (pod, node_id, pg_name)
    elif 'vpc' in add_type:
        x = node_id.split(',')
        node_1 = x[0]
        node_2 = x[1]
        tDn = 'topology/pod-%s/protpaths-%s-%s/pathep-[%s]' % (pod, node_1, node_2, pg_name)
        node_id = node_id.replace(',', '_')

    # Define File for adding static Path Binding and Open for Appending resources
    file_stbind = './fabric/resources_user_static_bindings_%s.tf' % (switch_ipr)
    afile = open(file_stbind, 'a+')

    # Verify if Static Binding Currently Exists or Not
    rsc_pg_to_epg = 'resource "aci_epg_to_static_path" "%s_%s_%s_%s_%s"' % (tenant, app, epg, node_id, pg_name)
    afile.seek(0)
    if not rsc_pg_to_epg in afile.read():
        # Add Static Path to static_path Resource File for Selected Switch
        afile.write('resource "aci_epg_to_static_path" "%s_%s_%s_%s_%s" {\n' % (tenant, app, epg, node_id, pg_name))
        afile.write('\tdepends_on           = [aci_application_epg.%s_%s_%s,aci_ranges.st_vlan_pool_add_%s]\n' % (tenant, app, epg, vlan))
        afile.write('\tapplication_epg_dn   = aci_application_epg.%s_%s_%s.id\n' % (tenant, app, epg))
        afile.write('\ttdn                  = "%s"\n' % (tDn))
        afile.write('\tencap                = "vlan-%s"\n' % (vlan))
        afile.write('\tmode                 = "%s"\n' % (vl_mode))
        afile.write('}\n\n')

    afile.close()

def resource_static_vlan_pool(vlan, wr_file):
    wr_file.write('resource "aci_ranges" "st_vlan_pool_add_%s" {\n' % (vlan))
    wr_file.write('\tvlan_pool_dn   = "uni/infra/vlanns-[access_vl-pool]-static"\n')
    wr_file.write('\t_from          = "vlan-%s"\n' % (vlan))
    wr_file.write('\tto		       = "vlan-%s"\n' % (vlan))
    wr_file.write('}\n\n')

def resource_tenant(tenant, tenant_descr):
    try:
        # Validate Tenant Name
        validating.name_rule(line_count, tenant)
    except Exception as err:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}.  Please verify input information.  Exiting....')
        print(f'\n-----------------------------------------------------------------------------\n')
        exit()
    
    # Build Template and Populate Template
    wr_file = wr_tenants
    wr_file.write('resource "aci_tenant" "%s" {\n' % (tenant))
    wr_file.write('\tdescription    = "%s"\n' % (tenant_descr))
    wr_file.write('\tname           = "%s"\n' % (tenant))
    wr_file.write('}\n\n')

def resource_vrf(tenant, vrf_name, vrf_desc, enforcement, enf_type):
    try:
        # Validate Tenant and VRF Name
        validating.name_rule(line_count, tenant)
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
    wr_file.write('\ttenant_dn                           = "uni/tn-%s"\n' % (tenant))
    wr_file.write('\tname                                = "%s"\n' % (vrf_name))
    wr_file.write('\tbd_enforced_enable                  = "yes"\n')
    wr_file.write('\tip_data_plane_learning			    = "enabled"\n')
    wr_file.write('\tpc_enf_pref						    = "%s"\n' % (enforcement))
    wr_file.write('\tpc_enf_dir						    = "ingress"\n')
    wr_file.write('\trelation_fv_rs_ctx_mon_pol		    = "uni/tn-common/monepg-default"\n')
    wr_file.write('\trelation_fv_rs_ctx_to_ep_ret		= "uni/tn-common/epRPol-default"\n')
    wr_file.write('\trelation_fv_rs_vrf_validation_pol   = "uni/tn-common/vrfvalidationpol-default"\n')
    wr_file.write('}\n\n')

    wr_file.write('resource "aci_any" "%s_any" {\n' % (vrf_name))
    wr_file.write('\tdepends_on                     = [aci_vrf.%s]\n' % (vrf_name))
    wr_file.write('\tvrf_dn                         = "uni/tn-%s/ctx-%s"\n' % (tenant, vrf_name))
    wr_file.write('\tdescription                    = "%s"\n' % (vrf_desc))

    if enf_type == 'preferred_group':
        wr_file.write('\tpref_gr_memb  				   = "enabled"\n')
        wr_file.write('}\n\n')
    elif enf_type == 'vzAny':
        wr_file.write('\tmatch_t      				   = "AtleastOne"\n')
        #wr_file.write('\trelation_vz_rs_any_to_cons = [data.aci_contract.default.id]\n')
        #wr_file.write('\trelation_vz_rs_any_to_prov	= [data.aci_contract.default.id]\n')
        wr_file.write('}\n\n')
    elif enf_type == 'contract':
        wr_file.write('}\n\n')

        # Define Variables for Template Creation - vzAny Contracts
        # Tenants > Networking > VRFs > {VRF Name} > EPG Collection for VRF: Provider/Consumer Contracts
        path_attrs = '/api/node/mo/uni/tn-%s/ctx-%s/any.json' % (tenant, vrf_name)
        depends_on = 'aci_vrf.%s' % (vrf_name)
        class_name_1 = 'vzRsAnyToCons'
        class_name_2 = 'vzRsAnyToProv'

        # Format Variables for JSON Output
        data_out_1 = {class_name_1: {'attributes': {'tnVzBrCPName': 'default'}}}
        data_out_2 = {class_name_2: {'attributes': {'tnVzBrCPName': 'default'}}}

        # Write Output to Resource Files using Template
        resrc_desc = 'vzAny_%s_Cons' % (vrf_name)
        tf_templates.aci_rest_depends_on(resrc_desc, depends_on, path_attrs, class_name_1, data_out_1, wr_file)
        resrc_desc = 'vzAny_%s_Prov' % (vrf_name)
        tf_templates.aci_rest_depends_on(resrc_desc, depends_on, path_attrs, class_name_2, data_out_2, wr_file)

def validate_pg_params(line_count, ws, add_type, read_tfstate, switch_ipr, int_select):
    try:
        # Check if Interface Profile Exists
        read_tfstate.seek(0)
        if add_type == 'add_vpc':
            xsw = switch_ipr.split(',')
            sw1 = xsw[0]
            sw2 = xsw[1]
            rsc_switch_ipr = '"id": "uni/infra/accportprof-%s"' % (sw1)
            if not rsc_switch_ipr in read_tfstate.read():
                validating.error_switch(line_count, ws, switch_ipr)
            rsc_switch_ipr = '"id": "uni/infra/accportprof-%s"' % (sw2)
            if not rsc_switch_ipr in read_tfstate.read():
                validating.error_switch(line_count, ws, switch_ipr)
        else:
            rsc_switch_ipr = '"id": "uni/infra/accportprof-%s"' % (switch_ipr)
            if not rsc_switch_ipr in read_tfstate.read():
                validating.error_switch(line_count, ws, switch_ipr)

        # Check if Interface Selector Exists
        read_tfstate.seek(0)
        rsc_int_select = '"id": "uni/infra/accportprof-%s/hports-%s-typ-range"' % (switch_ipr, int_select)
        if not rsc_int_select in read_tfstate.read():
            validating.error_int_selector(line_count, ws, int_select)
    except Exception as err:
        print(f'\n-----------------------------------------------------------------------------\n')
        print(f'   {SystemExit(err)}')
        print(f'   Error on Row {line_count}.  Please verify input information.  Exiting....')
        print(f'\n-----------------------------------------------------------------------------\n')
        exit()

def vlan_to_epg_mapping(line_count,vlan):
    vlan_count = 1
    app = ''
    epg = ''
    tenant = ''
    for rw in ws3.rows:
        if any(rw):
            add_type = str(rw[0].value)
            if add_type == 'add_to_apic':
                vlan_x = str(rw[7].value)
                if re.fullmatch('^[0-9]+$', vlan_x):
                    if int(vlan) == int(vlan_x):
                        #print (f'vlan x is "{vlan_x}"')
                        tenant = str(rw[1].value)
                        app = str(rw[5].value)
                        epg = str(rw[6].value)
                        vlan_count += 1
                        break
                    else:
                        vlan_count += 1
            else:
                vlan_count += 1
        else:
            vlan_count += 1
    #if app == '' or epg == '' or tenant == '':
    #    validating.error_vlan_to_epg(line_count, vlan, ws3)
    #else:
    return tenant,app,epg

line_count = 1
# Loop Through User Defined Tenants in Worksheet "Tenant"
for r in ws1.rows:
    if any(r):
        add_type = str(r[0].value)
        if add_type == 'add_tenant':
            tenant = str(r[1].value)
            tenant_descr = str(r[2].value)

            # Check if Tenant Already Exists and if Not Create Tenant
            if re.search('(common|infra|mgmt)', tenant):
                rsc_tenant = 'data "aci_tenant" "%s"' % (tenant)
            else:
                rsc_tenant = 'resource "aci_tenant" "%s"' % (tenant)
            wr_tenants.seek(0)
            if not rsc_tenant in wr_tenants.read():
                resource_tenant(tenant, tenant_descr)
            line_count += 1
        else:
            line_count += 1
    else:
        line_count += 1

line_count = 1
# Loop Through User Defined VRFs in Worksheet "VRF"
for r in ws2.rows:
    if any(r):        
        add_type = str(r[0].value)
        if add_type == 'add_vrf':
            tenant = str(r[1].value)
            vrf_name = str(r[2].value)
            vrf_desc = str(r[3].value)
            enforcement = str(r[4].value)
            enf_type = str(r[5].value)

            # Check if Tenant Exists
            if re.search('(common|infra|mgmt)', tenant):
                rsc_tenant = 'data "aci_tenant" "%s"' % (tenant)
            else:
                rsc_tenant = 'resource "aci_tenant" "%s"' % (tenant)
            wr_tenants.seek(0)
            if not rsc_tenant in wr_tenants.read():
                validating.error_tenant(line_count, tenant, ws1, ws2)

            # Check if VRF is Already Defined and if Not Create the VRF
            rsc_vrf = 'resource "aci_vrf" "%s"' % (vrf_name)
            wr_vrfs.seek(0)
            if not rsc_vrf in wr_vrfs.read():
                resource_vrf(tenant, vrf_name, vrf_desc, enforcement, enf_type)
            line_count += 1
        else:
            line_count += 1
    else:
        line_count += 1

line_count = 1
# Loop Through User Defined Tenants in Worksheet "App and EPG"
for r in ws3.rows:
    if any(r):
        add_type = str(r[0].value)
        if add_type == 'add_to_apic':
            tenant = str(r[1].value)
            bd = str(r[2].value)
            extend = str(r[3].value)
            vrf = str(r[4].value)
            app = str(r[5].value)
            epg = str(r[6].value)
            vlan = str(r[7].value)
            pvlan = str(r[8].value)
            priority = str(r[9].value)
            qos_policy = str(r[10].value)
            enforcement = str(r[11].value)
            enf_type = str(r[12].value)
            epg_descr = str(r[13].value)
            bd_descr = str(r[14].value)
            shut_down = str(r[15].value)

            # Need to get VRF Tenant and VRF Enforcement from VRF Worksheet
            line_count_holder = line_count
            line_count = 1
            vrf_enforcement = ''
            vrf_tenant = ''
            for rw in ws2.rows:
                if any(rw):
                    vrf_name = str(rw[2].value)
                    if vrf_name == vrf:
                        vrf_tenant = str(rw[1].value)
                        vrf_enforcement = str(rw[4].value)
                        line_count += 1
                        break
                    else:
                        line_count += 1
                else:
                    line_count += 1
            line_count = line_count_holder
            if vrf_tenant == '':
                validating.error_vrf(line_count, vrf)
            if vrf_enforcement == '':
                validating.error_enforce(line_count, vrf)
            elif vrf_enforcement == 'unenforced' and enforcement == 'enforced':
                validating.error_enforcement(line_count, epg, ws2, ws3)

            # Check if Bridge Domain Exists and if not Create it
            rsc_bd = 'resource "aci_bridge_domain" "%s"' % (bd)
            wr_bds.seek(0)
            if not rsc_bd in wr_bds.read():
                resource_bds(tenant, bd, bd_descr, extend, vrf)

            # Check if Application Exists and if not Create it
            rsc_app = 'resource "aci_application_profile" "%s_%s"' % (tenant, app)
            wr_apps.seek(0)
            if not rsc_app in wr_apps.read():
                resource_app(tenant, app, priority)

            # Check if Endpoint Group Exists and if not Create it
            rsc_epg = 'resource "aci_application_epg" "%s_%s_%s"' % (tenant, app, epg)
            wr_epgs.seek(0)
            if not rsc_epg in wr_epgs.read():
                resource_epg(tenant, bd, app, epg, priority, qos_policy, enforcement, enf_type, epg_descr, shut_down)
            line_count += 1
        else:
            line_count += 1
    else:
        line_count += 1

line_count = 1
# Loop Through User Defined L3Outs in Worksheet "L3Out"
for r in ws4.rows:
    if any(r):        
        add_type = str(r[0].value)
        if add_type == 'l3out':
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
# Loop Through User Defined Tenants in Worksheet "Tenant"
for r in ws7.rows:
    if any(r):
        add_type = str(r[0].value)
        if re.search('(_apg|_pcg|_vpc)', add_type):
            switch_ipr = str(r[1].value)
            int_select = str(r[2].value)
            aep = str(r[3].value)
            pg_name = str(r[4].value)
            lacp = str(r[5].value)
            mtu = str(r[6].value)
            speed = str(r[7].value)
            cdp = str(r[8].value)
            lldp = str(r[9].value)
            bpdu = str(r[10].value)
            pc_descr = str(r[12].value)
            descr = str(r[13].value)
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
            if '_pcg' in add_type:
                lag_type = 'node'
            elif '_vpc' in add_type:
                lag_type = 'link'
            
            if add_type == 'add_apg':
                resource_pgs_access(add_type, switch_ipr, int_select, pg_name, aep, mtu, speed, cdp, lldp, bpdu, descr)
            elif add_type == 'add_pcg':
                xs = switch_ipr.split(',')
                switch_ipr_1 = xs[0]
                switch_ipr_2 = xs[1]
                resource_pgs_bundle(add_type, switch_ipr_1, int_select, aep, pg_name, lacp, mtu, speed, cdp, lldp, bpdu, pc_descr, descr)
                resource_pgs_bundle(add_type, switch_ipr_2, int_select, aep, pg_name, lacp, mtu, speed, cdp, lldp, bpdu, pc_descr, descr)
            line_count += 1
        elif add_type == 'brk_out':
            switch_ipr = str(r[1].value)
            int_select = str(r[2].value)
            switch_role = str(r[3].value)
            model = str(r[4].value)
            module = str(r[5].value)
            brkout_pg = str(r[6].value)
            descr = str(r[13].value)
 
             # Create Resource Records for Port Groups
            resource_pgs_brkout(switch_ipr, int_select, switch_role, model, module, brkout_pg, descr)
            line_count += 1
        else:
            line_count += 1
    else:
        line_count += 1

line_count = 1
# Loop Through User Defined Tenants in Worksheet "Tenant"
for r in ws8.rows:
    if any(r):
        add_type = str(r[0].value)
        if re.search('(static)', add_type):
            pod = str(r[1].value)
            switch_ipr = str(r[2].value)
            node_id = str(r[3].value)
            pg_name = str(r[4].value)
            swpt_mode = str(r[5].value)
            native_vlan = str(r[6].value)
            trunk_vlans = str(r[7].value)
            
            # Create Resource Records for Static Paths
            loop_static_path_vlan_lists(line_count, add_type, pod, switch_ipr, node_id, pg_name, swpt_mode, native_vlan, trunk_vlans)
            line_count += 1
        else:
            line_count += 1
    else:
        line_count += 1

# Close out the Open Files
read_tfstate.close()
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