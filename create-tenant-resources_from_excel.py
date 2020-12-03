#!/usr/bin/env python3

import openpyxl
import ipaddress
import json
import phonenumbers
import os, re, sys, traceback, validators
import tf_templates
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
ws1 = wb['Access Interfaces']
ws2 = wb['Tenant']
ws3 = wb['VRF']
ws4 = wb['L3Out']
ws5 = wb['Bridge Domain']
ws6 = wb['Subnet']
ws7 = wb['DHCP Relay']
ws8 = wb['App and EPGs']

# Create Resource configuration Files to store user input Data
# resources_user_import_tntv.tf will include Tenant and VRF Definitions
# resources_user_import_bds.tf will include Bridge Domains, DHCP Relay and Subnets
# resources_user_import_epgs.tf will include Apps and EPGs
# resources_user_import_intf.tf
file_apps = './tenant/variables_user_import_apps.tf'
file_bds = './tenant/variables_user_import_bds.tf'
file_epgs = './tenant/variables_user_import_epgs.tf'
file_interfaces = './tenant/variables_user_import_access_interfaces.tf'
file_tenants = './tenant/resources_user_input_Tenants.tf'
file_vrfs = './tenant/resources_user_input_VRFs.tf'
wr_apps = open(file_apps, 'w')
wr_epgs = open(file_epgs, 'w')
wr_bds = open(file_bds, 'w')
wr_interfaces = open(file_interfaces, 'w')
wr_tenants = open(file_tenants, 'w')
wr_vrfs = open(file_vrfs, 'w')
wr_apps.write('# This File will include Applications\n\nvariable \"user_apps\" {\n\tdefault = {\n')
wr_epgs.write('# This File will include EPGs\n\nvariable \"user_epgs\" {\n\tdefault = {\n')
wr_bds.write('# This File will include Bridge Domains\n\nvariable \"user_bds\" {\n\tdefault = {\n')
wr_interfaces.write('# This File will include Access Interfaces\n\nvariable \"user_intfs\" {\n\tdefault = {\n')
wr_tenants.write("# This File will include Tenants\n\n")
wr_vrfs.write("# This File will include VRFs\n\n")

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
    wr_file.write('\ttenant_dn                          = "uni/tn-%s"\n' % (tenant_name))
    wr_file.write('\tname                               = "%s"\n' % (vrf_name))
    wr_file.write('\tbd_enforced_enable                 = "yes"\n')
    wr_file.write('\tip_data_plane_learning			    = "enabled"\n')
    wr_file.write('\tpc_enf_pref						= "enforced"\n')
    wr_file.write('\tpc_enf_dir						    = "ingress"\n')
    wr_file.write('\trelation_fv_rs_ctx_mon_pol		    = "uni/tn-common/monepg-default"\n')
    wr_file.write('\trelation_fv_rs_ctx_to_ep_ret		= "uni/tn-common/epRPol-default"\n')
    wr_file.write('\trelation_fv_rs_vrf_validation_pol  = "uni/tn-common/vrfvalidationpol-default"\n')
    wr_file.write('}\n\n')

    wr_file.write('resource "aci_any" "%s_any" {\n' % (vrf_name))
    wr_file.write('\tvrf_dn                         = "uni/tn-%s/ctx-%s"\n' % (tenant_name, vrf_name))
    wr_file.write('\tdescription                    = "%s"\n' % (vrf_desc))

    if fltr_type == 'pg':
        wr_file.write('\tpref_gr_memb  				= "enabled"\n')
        wr_file.write('}\n\n')
    elif fltr_type == 'vzAny':
        wr_file.write('\tmatch_t      				= "AtleastOne"\n')
        #wr_file.write('\trelation_vz_rs_any_to_cons = [data.aci_contract.default.id]\n')
        #wr_file.write('\trelation_vz_rs_any_to_prov	= [data.aci_contract.default.id]\n')
        wr_file.write('}\n\n')

        # Define Variables for Template Creation - vzAny Contracts
        # Tenants > Networking > VRFs > {VRF Name} > EPG Collection for VRF: Provider/Consumer Contracts
        path_attrs = '"/api/node/mo/uni/tn-{}/ctx-{}/any.json"'.format(tenant_name, vrf_name)
        class_name_1 = 'vzRsAnyToCons'
        class_name_2 = 'vzRsAnyToProv'

        # Format Variables for JSON Output
        data_out_1 = {class_name_1: {'attributes': {'tnVzBrCPName': 'default'}}}
        data_out_2 = {class_name_2: {'attributes': {'tnVzBrCPName': 'default'}}}

        # Write Output to Resource Files using Template
        resrc_desc = 'vzAny_{}_Cons'.format(vrf_name)
        tf_templates.aci_rest(resrc_desc, path_attrs, class_name_1, data_out_1, wr_file)
        resrc_desc = 'vzAny_{}_Prov'.format(vrf_name)
        tf_templates.aci_rest(resrc_desc, path_attrs, class_name_2, data_out_2, wr_file)

line_count = 0
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
            vrf_name = '{}_vrf'.format(tenant_name)
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

line_count = 0
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

line_count = 0
# Loop Through User Defined L3Outs in Worksheet "L3Out"
for r in ws2.rows:
    if any(r):        
        type = str(r[0].value)
        if type == 'l3out':
            l3_host_tnt = str(r[1].value)
            l3out_tenant = str(r[2].value)
            l3_domain = str(r[3].value)
            routing_pt = str(r[4].value)
            intf_type = str(r[5].value)

            # Create Resource Records for VRF
            resource_vrf(tnt_name, vrf_name, vrf_desc, fltr_type)
            line_count += 1
        else:
            line_count += 1
    else:
        line_count += 1

# Close out the Open Files
#csv_file.close()
wr_apps.write("\t}\n}")
wr_apps.close()
wr_epgs.write("\t}\n}")
wr_epgs.close()
wr_bds.write("\t}\n}")
wr_bds.close()
wr_interfaces.write("\t}\n}")
wr_interfaces.close()
wr_tenants.close()
wr_vrfs.close()


#End Script
print(f'\n-----------------------------------------------------------------------------\n')
print(f'   Completed Running Script.  Exiting....')
print(f'\n-----------------------------------------------------------------------------\n')
exit()