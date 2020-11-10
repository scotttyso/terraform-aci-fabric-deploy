import csv
import ipaddress
import os, re, sys, traceback, validators
from csv import reader
from csv import writer

re_desc = re.compile('^  description (.+)$')
re_host = re.compile('^hostname ([a-zA-Z0-9\\-\\_\\.]+)$')
re_intf = re.compile('^interface ((port\\-channel\\d+|Ethernet\\d+[\\d\\/]+))$')
re_mtu_ = re.compile('^  mtu (\\d+)$')
re_poch = re.compile('^  channel-group (\\d+) mode ((active|on|passive))$')
re_swav = re.compile('^  switchport access vlan (\\d+)$')
re_tknv = re.compile('^  switchport trunk native vlan (\\d{1,4})$')
re_tkv1 = re.compile('^  switchport trunk allowed vlan (\\d{1,4}[\\-,]+.+\\d{1,4})$')
re_tkv2 = re.compile('^  switchport trunk allowed vlan (\\d{1,4})$')
re_vpc_ = re.compile('^  vpc ((\\d+|peer\\-link))$')

def function_re_swav(line):
    search_swav = re.search('^  switchport access vlan (\\d+)$', line)
    return search_swav.group(1)

def function_re_host(line):
    search_host = re.search('^hostname ([a-zA-Z0-9\\-\\_\\.]+$)', line)
    return search_host.group(1)

def function_re_intf(line):
    search_intf = re.search('^interface ((port\\-channel\\d+|Ethernet\\d+[\\d\\/]+))$', line)
    return search_intf.group(1)

def function_re_desc(line):
    search_desc = re.search('^  description (.+)$', line)
    return search_desc.group(1)

def function_re_mtu_(line):
    search_mtu_ = re.search('^  mtu (\\d+)$', line)
    return search_mtu_.group(1)

def function_re_poch(line):
    search_poch = re.search('^  channel-group (\\d+) mode ((active|on|passive))$', line)
    return search_poch.group(1),search_poch.group(2)

def function_re_tknv(line):
    search_tknv = re.search('^  switchport trunk native vlan (\\d{1,4})$', line)
    return search_tknv.group(1)

def function_re_tkv1(line):
    search_tkvl = re.search('^  switchport trunk allowed vlan (\\d{1,4}[\\-,]+.+\\d{1,4})$', line)
    return search_tkvl.group(1)

def function_re_tkv2(line):
    search_tkvl = re.search('^  switchport trunk allowed vlan (\\d{1,4})$', line)
    return search_tkvl.group(1)

def function_re_vpc_(line):
    search_vpc_ = re.search('^  vpc ((\\d+|peer\\-link))$', line)
    return search_vpc_.group(1)

# Start by Creating Default Variable Values
str_bpdg = 'no'
str_cdp_ = 'no'
str_desc = ''
str_host = 'undefined'
str_intf = ''
str_lldr = 'no'
str_lldt = 'no'
str_mtu_ = 'undefined'
str_poch = 'undefined'
str_pomd = 'undefined'
str_swav = '1'
str_swmd = 'access'
str_swpt = 'no'
str_tknv = '1'
str_tkvl = 'undefined'
str_vpc_ = 'undefined'

# Import the Configuration File
file = open('143b-core01.cfg', 'r')
wr_poch = open('int_poch.csv', 'w')
wr_intf = open('int_swpt.csv', 'w')

# Read the Conifguration File and Gather Vlan Information
lines = file.readlines()

line_count = 0
ethn_count = 0
for line in lines:
    if re.search(re_host, line):
        # Found an Interface
        str_host = function_re_host(line)
        line_count += 1
    elif re.search(re_intf, line):
        # Found an Interface
        str_intf = function_re_intf(line)
        line_count += 1
    elif re.search('^  spanning-tree bpduguard enable$', line):
        str_bpdg = 'yes'
        line_count += 1
    elif re.search('^  cdp enable$', line):
        str_cdp_ = 'yes'
        line_count += 1
    elif re.search('^  lldp receive$', line):
        str_lldr = 'yes'
        line_count += 1
    elif re.search('^  lldp transmit$', line):
        str_lldt = 'yes'
        line_count += 1
    elif re.search(re_swav, line):
        # Access VLAN
        str_swav = function_re_swav(line)
    elif re.search('^  switchport mode access$', line):
        # Interface is a switchport
        str_swmd = 'access'
    elif re.search('^  switchport mode trunk$', line):
        # Interface is a switchport
        str_swmd = 'trunk'
    elif re.search(re_tknv, line):
        # Trunk Native VLAN
        str_tknv = function_re_tknv(line)
        line_count += 1
    elif re.search(re_tkv1, line):
        # Trunk Vlan List
        str_tkvl = function_re_tkv1(line)
        line_count += 1
    elif re.search(re_tkv2, line):
        # Trunk Vlan List
        str_tkvl = function_re_tkv2(line)
        line_count += 1
    elif re.search('^  switchport$', line):
        # Interface is a switchport
        str_swpt = 'yes'
    elif re.search(re_mtu_, line):
        # Found MTU Defined in
        str_mtu_ = function_re_mtu_(line)
        line_count += 1
    elif re.search(re_poch, line):
        # Found the VLAN name
        str_poch,str_pomd = function_re_poch(line)
        line_count += 1
    elif re.search(re_vpc_, line):
        # Found VPC_id on Port-Channel
        str_vpc_ = function_re_vpc_(line)
        line_count += 1
    elif re.search(re_desc, line):
        # Found a Description on the Interface
        str_desc = function_re_desc(line)
        line_count += 1
    elif line == "\n":
        # Found blank line, which means the end of the interface, time to create the output
        if 'channel' in str_intf:
            if str_swpt == 'yes':
                if re.search('[,]+', str_tkvl):
                    str_tkvl = str_tkvl.replace(',', '_')
                if re.search('[,]+', str_desc):
                    str_desc = str_desc.replace(',', '_')
                wr_poch.write('{},{},{},{},{},{},{},{},{}\n'.format(str_host, str_intf, str_vpc_, str_mtu_, str_swmd, str_swav, str_tknv, 
                              str_tkvl, str_desc))
        elif 'Ethernet' in str_intf:
            if ethn_count == 0:
                wr_poch.close()
                wr_intf.write('Type,New Host,New Interface,Current Host,Current Interface,Port Type ,port-channel ID,VPC_ID,MTU,Switchport Mode,\
                              Access VLAN or Native VLAN,Trunk Allowed VLANs,CDP Enabled,LLDP Receive,LLDP Transmit,BPDU Guard,\
                              Port-Channel Description,Port Description\n')
                wr_poch = open('int_poch.csv', 'r')
                po_lines = wr_poch.readlines()
                ethn_count += 1
            if str_swpt == 'yes':
                if re.search('(\\d+|peer)', str_poch):
                    for line in po_lines:
                        x = line.split(',')
                        desc = x[8].strip()
                        if str_poch in x[1]:
                            if x[3] == 'undefined':
                                if str_swmd == 'access':
                                    wr_intf.write('intf_add,,,{},{},pc,{},n/a,{},{},{},{},n/a,{},{},{},{},{}\n'.format(str_host, str_intf, str_poch, x[3], 
                                                  x[4], x[5], str_cdp_, str_lldr, str_lldt, str_bpdg, desc, str_desc))
                                elif str_swmd == 'trunk':
                                    wr_intf.write('intf_add,,,{},{},pc,{},n/a,{},{},{},{},{},{},{},{},{},{}\n'.format(str_host, str_intf, str_poch, x[3], 
                                                  x[4], x[6], x[7], str_cdp_, str_lldr, str_lldt, str_bpdg, desc, str_desc))
                            else:
                                if str_swmd == 'access':
                                    wr_intf.write('intf_add,,,{},{},vpc,{},{},{},{},{},{},n/a,{},{},{},{},{}\n'.format(str_host, str_intf, str_poch, x[2], 
                                                  x[3], x[4], x[5], str_cdp_, str_lldr, str_lldt, str_bpdg, desc, str_desc))
                                elif str_swmd == 'trunk':
                                    wr_intf.write('intf_add,,,{},{},vpc,{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(str_host, str_intf, str_poch, x[2], 
                                                  x[3], x[4], x[6], x[7], str_cdp_, str_lldr, str_lldt, str_bpdg, desc, str_desc))
                else:
                    if re.search('[,]+', str_tkvl):
                        str_tkvl = str_tkvl.replace(',', '_')
                    if re.search('[,]+', str_desc):
                        str_desc = str_desc.replace(',', '_')
                    if str_swmd == 'access':
                        wr_intf.write('intf_add,,,{},{},ap,n/a,n/a,{},{},{},n/a,{},{},{},{},n/a,{}\n'.format(str_host, str_intf, str_mtu_, str_swmd, 
                                      str_swav, str_cdp_, str_lldr, str_lldt, str_bpdg, str_desc))
                    elif str_swmd == 'trunk':
                        wr_intf.write('intf_add,,,{},{},ap,n/a,n/a,{},{},{},{},{},{},{},{},n/a,{}\n'.format(str_host, str_intf, str_mtu_, str_swmd, 
                                      str_tknv, str_tkvl, str_cdp_, str_lldr, str_lldt, str_bpdg, str_desc))

        
        # Reset the Variables back to Default
        str_bpdg = 'no'
        str_cdp_ = 'no'
        str_desc = ''
        str_intf = ''
        str_lldr = 'no'
        str_lldt = 'no'
        str_mtu_ = 'undefined'
        str_poch = 'undefined'
        str_pomd = 'undefined'
        str_swav = '1'
        str_swmd = 'access'
        str_swpt = 'no'
        str_tknv = '1'
        str_tkvl = 'undefined'
        str_vpc_ = 'undefined'
        line_count += 1
    else:
        line_count += 1


file.close()
wr_poch.close()
wr_intf.close()

remove_poch_file = 'rm int_poch.csv'
os.system(remove_poch_file)

print('end script')