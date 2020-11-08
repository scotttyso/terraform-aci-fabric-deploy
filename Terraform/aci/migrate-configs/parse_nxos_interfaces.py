import csv
import ipaddress
import os, re, sys, traceback, validators
from csv import reader
from csv import writer

re_acvl = re.compile('^  switchport access vlan (\d+)$')
re_host = re.compile('^hostname ([a-zA-Z0-9\-\_\.]+)$')
re_intf = re.compile('^interface ((port\-channel\d+|Ethernet\d+[\d\/]+))$')
re_desc = re.compile('^  description (.+)$')
re_mtud = re.compile('^  mtu (\d+)$')
re_poch = re.compile('^  channel-group (\d+) mode ((active|on|passive))$')
re_tkv1 = re.compile('^  switchport trunk allowed vlan (\d{1,4}[\-,]+.+\d{1,4})$')
re_tkv2 = re.compile('^  switchport trunk allowed vlan (\d{1,4})$')
re_vpcd = re.compile('^  vpc ((\d+|peer\-link))$')

def function_re_acvl(line):
    search_acvl = re.search('^  switchport access vlan (\d+)$', line)
    return search_acvl.group(1)

def function_re_host(line):
    search_host = re.search('^hostname ([a-zA-Z0-9\-\_\.]+$)', line)
    return search_host.group(1)

def function_re_intf(line):
    search_intf = re.search('^interface ((port\-channel\d+|Ethernet\d+[\d\/]+))$', line)
    return search_intf.group(1)

def function_re_desc(line):
    search_desc = re.search('^  description (.+)$', line)
    return search_desc.group(1)

def function_re_mtud(line):
    search_mtud = re.search('^  mtu (\d+)$', line)
    return search_mtud.group(1)

def function_re_poch(line):
    search_poch = re.search('^  channel-group (\d+) mode ((active|on|passive))$', line)
    return search_poch.group(1),search_poch.group(2)

def function_re_tkv1(line):
    search_tkvl = re.search('^  switchport trunk allowed vlan (\d{1,4}[\-,]+.+\d{1,4})$', line)
    return search_tkvl.group(1)

def function_re_tkv2(line):
    search_tkvl = re.search('^  switchport trunk allowed vlan (\d{1,4})$', line)
    return search_tkvl.group(1)

def function_re_vpcd(line):
    search_vpcd = re.search('^  vpc ((\d+|peer\-link))$', line)
    return search_vpcd.group(1)

# Start by Creating Default Variable Values
str_host = 'undefined'
str_acvl = 'undefined'
str_intf = ''
str_desc = ''
str_mtud = 'undefined'
str_poch = 'undefined'
str_mode = ''
str_swpt = 'no'
str_tkvl = 'undefined'
str_trnk = 'no'
str_vpcd = 'undefined'

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
    elif re.search(re_acvl, line):
        # Access VLAN
        str_acvl = function_re_acvl(line)
    elif '  switchport mode trunk' in line:
        # Interface is a switchport
        str_trnk = 'yes'
    elif re.search(re_tkv1, line):
        # Trunk Vlan List
        str_tkvl = function_re_tkv1(line)
        line_count += 1
    elif re.search(re_tkv2, line):
        # Trunk Vlan List
        str_tkvl = function_re_tkv2(line)
        line_count += 1
    elif '  switchport' in line:
        # Interface is a switchport
        str_swpt = 'yes'
    elif re.search(re_mtud, line):
        # Found MTU Defined in
        str_mtud = function_re_mtud(line)
        line_count += 1
    elif re.search(re_poch, line):
        # Found the VLAN name
        str_poch,str_mode = function_re_poch(line)
        line_count += 1
    elif re.search(re_vpcd, line):
        # Found VPC_id on Port-Channel
        str_vpcd = function_re_vpcd(line)
        line_count += 1
    elif re.search(re_desc, line):
        # Found a Description on the Interface
        str_desc = function_re_desc(line)
        line_count += 1
    elif line == "\n":
        # Found blank line, which means the end of the interface, time to create the output
        if 'channel' in str_intf:
            if str_swpt == 'yes':
                wr_poch.write('{}|{}|{}|{}|{}|{}|{}|{}\n'.format(str_host, str_intf, str_vpcd, str_trnk, str_tkvl, str_acvl, str_mtud, str_desc))
        elif 'Ethernet' in str_intf:
            if ethn_count == 0:
                wr_poch.close()
                wr_poch = open('int_poch.csv', 'r')
                po_lines = wr_poch.readlines()
                ethn_count += 1
            if str_swpt == 'yes':
                if re.search('(\d+|peer)', str_poch):
                    for line in po_lines:
                        x = line.split('|')
                        desc = x[7].strip()
                        if str_poch in x[1]:
                            if x[2] == 'undefined':
                                wr_intf.write('intf_add|pc|{}||{}|{}|{}|{}|{}|{}|none|{}|{}\n'.format(str_host, str_intf, str_poch, x[3], x[4], x[5], x[6], desc, str_desc))
                            else:
                                wr_intf.write('intf_add|vpc|{}||{}|{}|{}|{}|{}|{}|{}|{}|{}\n'.format(str_host, str_intf, str_poch, x[3], x[4], x[5], x[6], x[2], desc, str_desc))
                else:
                    wr_intf.write('intf_add|ap|{}|{}|{}|{}|{}|{}|{}\n'.format(str_host, str_intf, str_trnk, str_tkvl, str_acvl, str_mtud, str_desc))
        
        # Reset the Variables back to Default
        str_intf = ''
        str_acvl = 'undefined'
        str_desc = ''
        str_mtud = 'undefined'
        str_poch = 'undefined'
        str_mode = ''
        str_swpt = 'no'
        str_tkvl = 'undefined'
        str_trnk = 'no'
        str_vpcd = 'undefined'
        line_count += 1
    else:
        line_count += 1


file.close()
wr_poch.close()
wr_intf.close()

remove_poch_file = 'rm int_poch.csv'
os.system(remove_poch_file)

print('end script')