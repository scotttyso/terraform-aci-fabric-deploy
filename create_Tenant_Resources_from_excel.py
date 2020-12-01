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
file_apps = './tenant/variables_user_import_apps.tf'
file_bds = './tenant/variables_user_import_bds.tf'
file_epgs = './tenant/variables_user_import_epgs.tf'
file_interfaces = './tenant/variables_user_import_access_interfaces.tf'
file_tenants = './tenant/variables_user_import_Tenants.tf'
file_vrfs = './tenant/variables_user_import_VRFs.tf'
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
wr_tenants.write("# This File will include Tenants\n\nvariable \"user_tenants\" {\n\tdefault = {\n")
wr_vrfs.write("# This File will include VRFs\n\nvariable \"user_vrfs\" {\n\tdefault = {\n")

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
    payload_form = '\t\t"{0}" = {1}\n\t\t\t{2} = "{3}"\n\t\t\t{4} = "{5}"\n\t\t{6}\n'
    wr_to_file = payload_form.format(tenant_name, "{", 'description', tenant_descr, 'name', tenant_name, "},")

    # Write Data to Varialbles File
    wr_tenants.write(wr_to_file)

def resource_vrf(tenant_name, vrf_name):
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
    payload_form = '\t\t"{0}" = {1}\n\t\t\t{2} = "{3}"\n\t\t\t{4} = "{5}"\n\t\t{6}\n'
    wr_to_file = payload_form.format(vrf_name, "{", 'tenant', tenant_name, 'name', vrf_name, "},")

    # Write Data to Varialbles File
    wr_vrfs.write(wr_to_file)



line_count = 0
# Loop Through User Defined Tenants in Worksheet 1
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
            vrf_desc = str(r[3].value)
            fltr_type = str(r[4].value)

            # Create Resource Records for Tenant
            resource_tenant(tenant_name, tenant_desc)
            tnt_name = 'common'
            resource_vrf(tnt_name, vrf_name)
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
wr_tenants.write("\t}\n}")
wr_tenants.close()
wr_vrfs.write("\t}\n}")
wr_vrfs.close()


#End Script
print(f'\n-----------------------------------------------------------------------------\n')
print(f'   Completed Running Script.  Exiting....')
print(f'\n-----------------------------------------------------------------------------\n')
exit()