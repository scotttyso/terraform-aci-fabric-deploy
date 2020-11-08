import csv
import ipaddress
import os, re, sys, traceback, validators
from csv import reader
from csv import writer

re_dhcp = re.compile('^  ip dhcp relay address (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})$')
re_desc = re.compile('^  description (.+)$')
re_hsv4 = re.compile('^    ip (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})$')
re_hsv4_sec = re.compile('^    ip (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}) secondary$')
re_ipv4 = re.compile('^  ip address (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}(?:/\d{1,2}|))$')
re_ipv4_sec = re.compile('^  ip address (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}(?:/\d{1,2}|)) secondary$')
re_ivln = re.compile('^interface Vlan([0-9]+)$')
re_vlan = re.compile('^vlan (\d{1,4})$')
re_vlan_list = re.compile('^vlan (\d{1,4}[\-,]+.+\d{1,4})$')
re_vlan_name = re.compile('^  name (.+)$')
re_vrfd = re.compile('^  vrf member (.+)$')

def function_dhcp(line):
    search_dhcp = re.search('^  ip dhcp relay address (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})$', line)
    return search_dhcp.group(1)

def function_desc(line):
    search_desc = re.search('^  description (.+)$', line)
    return search_desc.group(1)

def function_hsv4(line):
    search_hsv4 = re.search('^    ip (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})$', line)
    return search_hsv4.group(1)

def function_hsv4_sec(line):
    search_hsv4_sec = re.search('^    ip (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}) secondary$', line)
    return search_hsv4_sec.group(1)

def function_ipv4(line):
    search_ipv4 = re.search('^  ip address (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}(?:/\d{1,2}|))$', line)
    return search_ipv4.group(1)

def function_ipv4_sec(line):
    search_ipv4_sec = re.search('^  ip address (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}(?:/\d{1,2}|)) secondary$', line)
    return search_ipv4_sec.group(1)

def function_ivln(line):
    search_ivln = re.search('^interface Vlan([0-9]+)$', line)
    return search_ivln.group(1)

def function_vlan(line):
    search_vlan = re.search('^vlan (\d{1,4})$', line)
    return search_vlan.group(1)

def function_vlan_name(line):
    search_vlan_name = re.search('^  name (.+)$', line)
    return search_vlan_name.group(1)

def function_vlan_list(line):
    search_vlan_list = re.search('^vlan (\d{1,4}[\-,]+.+\d{1,4})$', line)
    return search_vlan_list.group(1)

def function_vrfd(line):
    search_vrfd = re.search('^  vrf member (.+)$', line)
    return search_vrfd.group(1)

def function_wr_vlan(vlan):
    if vlan < 10:
        vlan = str(vlan)
        wr_vlan.write('v000{}_bd\n'.format(vlan))
    elif vlan < 100:
        vlan = str(vlan)
        wr_vlan.write('v00{}_bd\n'.format(vlan))
    elif vlan < 1000:
        vlan = str(vlan)
        wr_vlan.write('v0{}_bd\n'.format(vlan))
    else:
        vlan = str(vlan)
        wr_vlan.write('v{}_bd\n'.format(vlan))

def function_wr_name(vlan,name):
    if vlan < 10:
        wr_name.write('v000{}_bd,{}\n'.format(vlan, name))
    elif vlan < 100:
        vlan = str(vlan)
        wr_name.write('v00{}_bd,{}\n'.format(vlan, name))
    elif vlan < 1000:
        vlan = str(vlan)
        wr_name.write('v0{}_bd,{}\n'.format(vlan, name))
    else:
        vlan = str(vlan)
        wr_name.write('v{}_bd,{}\n'.format(vlan, name))

def function_vlan_to_bd(vlan):
    if vlan < 10:
        vlan = str(vlan)
        bd = 'v000' + vlan + '_bd'
        return bd
    elif vlan < 100:
        vlan = str(vlan)
        bd = 'v00' + vlan + '_bd'
        return bd
    elif vlan < 1000:
        vlan = str(vlan)
        bd = 'v0' + vlan + '_bd'
        return bd
    else:
        vlan = str(vlan)
        bd = 'v' + vlan + '_bd'
        return bd

def function_expand_vlan_list(vlan_list):
    vlist = str_vlan_list.split(',')
    for v in vlist:
        if re.search('^\d{1,4}\-\d{1,4}$', v):
            a,b = v.split('-')
            a = int(a)
            b = int(b)
            vrange = range(a,b+1)
            for vl in vrange:
                function_wr_vlan(vl)
        elif re.search('^\d{1,4}$', v):
            v = int(v)
            function_wr_vlan(v)
    

# Start by Creating Empty Variables
str_dhcp = ''
str_desc = ''
str_hsv4 = ''
str_hsv4_sec = ''
str_ipv4 = ''
str_ipv4_sec = ''
str_ivln = ''
str_vlan = ''
str_vlan_list = ''
str_vlan_name = ''
str_vrfd = ''

# Import the Configuration File
file = open('143b-core01.cfg', 'r')
wr_vlan = open('vlan_list.csv', 'w')
wr_name = open('vlan_name.csv', 'w')
wr_ivln = open('gtwy_list.csv', 'w')
wr_dhcp = open('dhcp.csv', 'w')

# Read the Conifguration File and Gather Vlan Information
lines = file.readlines()

wr_ivln.write('type|int_type|Bridge_Domain|Gateway IPv4|vrf|Description\n')

line_count = 0
for line in lines:
    if re.search(re_vlan_list, line):
        # Found the Vlan List
        str_vlan_list = function_vlan_list(line)
        function_expand_vlan_list(str_vlan_list)
        line_count += 1
    elif re.search(re_vlan, line):
        # Found a VLAN
        str_vlan = function_vlan(line)
        str_vlan = int(str_vlan)
        line_count += 1
    elif re.search(re_vlan_name, line):
        # Found the VLAN name
        str_vlan_name = function_vlan_name(line)
        function_wr_name(str_vlan,str_vlan_name)
        #print(f'vlan is {str_vlan} and name is {str_vlan_name}')
        line_count += 1
    elif re.search(re_ivln, line):
        # Found the Vlan Interface
        str_ivln = function_ivln(line)
        str_ivln = int(str_ivln)
        line_count += 1
    elif re.search(re_vrfd, line):
        # Found VRF on the Interface
        str_vrfd = function_vrfd(line)
        line_count += 1
    elif re.search(re_ipv4, line):
        # Found IPv4 Address on the Interface
        str_ipv4 = function_ipv4(line)
        line_count += 1
    elif re.search(re_ipv4_sec, line):
        # Found IPv4 Secondary Address on the Interface
        str_ipv4_sec = function_ipv4_sec(line)
        line_count += 1
    elif re.search(re_hsv4, line):
        # Found IPv4 Address on the Interface
        str_hsv4 = function_hsv4(line)
        line_count += 1
    elif re.search(re_hsv4_sec, line):
        # Found IPv4 Secondary Address on the Interface
        str_hsv4_sec = function_hsv4_sec(line)
        line_count += 1
    elif re.search(re_dhcp, line):
        # Found IPv4 Secondary Address on the Interface
        str_dhcp = function_dhcp(line)
        if str_vrfd:
            wr_dhcp.write('dhcp_relay|{}|{}\n'.format(str_dhcp, str_vrfd))
        else:
            wr_dhcp.write('dhcp_relay|{}|default\n'.format(str_dhcp))
        line_count += 1
    elif re.search(re_desc, line):
        # Found a Description on the Interface
        str_desc = function_desc(line)
        line_count += 1
    elif line == "\n":
        # Found blank line, which means the end of the interface, time to create the output
        if not str_desc:
            str_desc = 'undefined'
        if not str_ipv4:
            line_count += 1
        elif str_ipv4:
            bd = function_vlan_to_bd(str_ivln)
            check_ipv4 = ipaddress.IPv4Interface(str_ipv4)
            network_v4 = check_ipv4.network
            if str_hsv4:
                a,b = str_ipv4.split('/')
                gtwy = str(str_hsv4) + '/' + str(b)
            else:
                gtwy = str(str_ipv4)
            if str_vrfd:
                wr_ivln.write('subnet_add|primary|{}|{}|{}|{}\n'.format(bd, gtwy, str_vrfd, str_desc))
            else:
                wr_ivln.write('subnet_add|primary|{}|{}|default|{}\n'.format(bd, gtwy, str_desc))
            if str_ipv4_sec:
                if str_hsv4_sec:
                    a,b = str_ipv4_sec.split('/')
                    gtwy = str(str_hsv4_sec) + '/' + str(b)
                else:
                    gtwy = str(str_ipv4)
                if str_vrfd:
                    wr_ivln.write('subnet_add|secondary|{}|{}|{}|{}\n'.format(bd, gtwy, str_vrfd, str_desc))
                else:
                    wr_ivln.write('subnet_add|secondary|{}|{}|default|{}\n'.format(bd, gtwy, str_desc))
            line_count += 1
        
        # Reset the Variables back to Blank
        str_dhcp = ''
        str_desc = ''
        str_hsv4 = ''
        str_hsv4_sec = ''
        str_ipv4 = ''
        str_ipv4_sec = ''
        str_ivln = ''
        str_vrfd = ''
    else:
        line_count += 1


file.close()
wr_vlan.close()
wr_name.close()
wr_ivln.close()
wr_dhcp.close()

#Get VLAN's that don't have a name and those that do and combine into one file
vlan_line_count = len(open('vlan_list.csv').readlines(  ))
bg_list_1 = open('vlan_list.csv', 'r') 
bg_list_2 = open('vlan_name.csv', 'r')
bg_list_3 = open('vlan_comb.csv', 'w')
vlan_lines = bg_list_1.readlines()
name_lines = bg_list_2.readlines()
for lineg1 in vlan_lines:
    matched = 0
    lineg1 = lineg1.strip()
    for lineg2 in name_lines:
        lineg2 = lineg2.strip()
        if lineg1 in lineg2:
            matched +=1
    if matched == 0:
        bg_list_3.write('{}\n'.format(lineg1))
        #print(x,y)
for line in name_lines:
    line.strip()
    bg_list_3.write('{}'.format(line))

bg_list_1.close()
bg_list_2.close()
bg_list_3.close()

#Sort the combined VLANs in final output file
bg_list_3 = open('vlan_comb.csv', 'r')
bg_list_4 = open('vlan_bddm.csv', 'w')
bg_list_4.write('type|bd_type|Bridge_Domain|Description\n')
bddm = bg_list_3.readlines()
bddm.sort()
for line in range(len(bddm)):
    bddm[line]
    bg_list_4.write('bd_add|extend_out|{}'.format(bddm[line]))

bg_list_3.close()
bg_list_4.close()

dhcp_relay_uniq = 'cat dhcp.csv | sort | uniq > dhcp_sort.csv'
dhcp_relay_add_header = 'echo "type|Relay Address|vrf" | cat - dhcp_sort.csv > dhcp_relay.csv'
remove_extra_dhcp_file1 = 'rm dhcp.csv'
remove_extra_dhcp_file2 = 'rm dhcp_sort.csv'
remove_extra_vlan_file1 = 'rm vlan_comb.csv'
remove_extra_vlan_file2 = 'rm vlan_list.csv'
remove_extra_vlan_file3 = 'rm vlan_name.csv'
os.system(dhcp_relay_uniq)
os.system(dhcp_relay_add_header)
os.system(remove_extra_dhcp_file1)
os.system(remove_extra_dhcp_file2)
os.system(remove_extra_vlan_file1)
os.system(remove_extra_vlan_file2)
os.system(remove_extra_vlan_file3)


print('end script')