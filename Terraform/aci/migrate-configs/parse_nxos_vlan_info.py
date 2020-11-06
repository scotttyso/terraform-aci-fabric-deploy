import csv
import ipaddress
import os, re, sys, traceback, validators
from csv import reader
from csv import writer

re_dhcp = re.compile('^  ip dhcp relay address (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})$')
re_desc = re.compile('^  description (.+)$')
re_hsrpv4 = re.compile('^    ip (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})$')
re_hsrpv4_sec = re.compile('^    ip (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}) secondary$')
re_ipv4 = re.compile('^  ip address (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}(?:/\d{1,2}|))$')
re_ipv4_sec = re.compile('^  ip address (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}(?:/\d{1,2}|)) secondary$')
re_ivlan = re.compile('^interface Vlan([0-9]+)$')
re_vlan = re.compile('^vlan (\d{1,4})$')
re_vlan_list = re.compile('^vlan (\d{1,4}[\-,]+.+\d{1,4})$')
re_vlan_name = re.compile('^  name (.+)$')
re_vrf = re.compile('^  vrf member (.+)$')

def function_dhcp(line):
    search_dhcp = re.search('^  ip dhcp relay address (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})$', line)
    return search_dhcp.group(1)

def function_desc(line):
    search_desc = re.search('^  description (.+)$', line)
    return search_desc.group(1)

def function_hsrpv4(line):
    search_hsrpv4 = re.search('^    ip (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})$', line)
    return search_hsrpv4.group(1)

def function_hsrpv4_sec(line):
    search_hsrpv4_sec = re.search('^    ip (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}) secondary$', line)
    return search_hsrpv4_sec.group(1)

def function_ipv4(line):
    search_ipv4 = re.search('^  ip address (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}(?:/\d{1,2}|))$', line)
    return search_ipv4.group(1)

def function_ipv4_sec(line):
    search_ipv4_sec = re.search('^  ip address (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}(?:/\d{1,2}|)) secondary$', line)
    return search_ipv4_sec.group(1)

def function_ivlan(line):
    search_ivlan = re.search('^interface Vlan([0-9]+)$', line)
    return search_ivlan.group(1)

def function_vlan(line):
    search_vlan = re.search('^vlan (\d{1,4})$', line)
    return search_vlan.group(1)

def function_vlan_name(line):
    search_vlan_name = re.search('^  name (.+)$', line)
    return search_vlan_name.group(1)

def function_vlan_list(line):
    search_vlan_list = re.search('^vlan (\d{1,4}[\-,]+.+\d{1,4})$', line)
    return search_vlan_list.group(1)

def function_vrf(line):
    search_vrf = re.search('^  vrf member (.+)$', line)
    return search_vrf.group(1)

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
    vlist = string_vlan_list.split(',')
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
string_dhcp = ''
string_desc = ''
string_hsrpv4 = ''
string_hsrpv4_sec = ''
string_ipv4 = ''
string_ipv4_sec = ''
string_ivlan = ''
string_vlan = ''
string_vlan_list = ''
string_vlan_name = ''
string_vrf = ''

# Import the Configuration File
file = open('143b-core01.cfg', 'r')
wr_vlan = open('vlan_list.csv', 'w')
wr_name = open('vlan_name.csv', 'w')
wr_ivlan = open('gtwy_list.csv', 'w')
wr_dhcp = open('dhcp.csv', 'w')

# Read the Conifguration File and Gather Vlan Information
lines = file.readlines()

wr_ivlan.write('type,int_type,Bridge_Domain,Gateway IPv4,VRF,Description\n')

line_count = 0
for line in lines:
    if re.search(re_vlan_list, line):
        # Found the Vlan List
        string_vlan_list = function_vlan_list(line)
        function_expand_vlan_list(string_vlan_list)
        line_count += 1
    elif re.search(re_vlan, line):
        # Found a VLAN
        string_vlan = function_vlan(line)
        string_vlan = int(string_vlan)
        line_count += 1
    elif re.search(re_vlan_name, line):
        # Found the VLAN name
        string_vlan_name = function_vlan_name(line)
        function_wr_name(string_vlan,string_vlan_name)
        #print(f'vlan is {string_vlan} and name is {string_vlan_name}')
        line_count += 1
    elif re.search(re_ivlan, line):
        # Found the Vlan Interface
        string_ivlan = function_ivlan(line)
        string_ivlan = int(string_ivlan)
        line_count += 1
    elif re.search(re_vrf, line):
        # Found vrf on the Interface
        string_vrf = function_vrf(line)
        line_count += 1
    elif re.search(re_ipv4, line):
        # Found IPv4 Address on the Interface
        string_ipv4 = function_ipv4(line)
        line_count += 1
    elif re.search(re_ipv4_sec, line):
        # Found IPv4 Secondary Address on the Interface
        string_ipv4_sec = function_ipv4_sec(line)
        line_count += 1
    elif re.search(re_hsrpv4, line):
        # Found IPv4 Address on the Interface
        string_hsrpv4 = function_hsrpv4(line)
        line_count += 1
    elif re.search(re_hsrpv4_sec, line):
        # Found IPv4 Secondary Address on the Interface
        string_hsrpv4_sec = function_hsrpv4_sec(line)
        line_count += 1
    elif re.search(re_dhcp, line):
        # Found IPv4 Secondary Address on the Interface
        string_dhcp = function_dhcp(line)
        if string_vrf:
            wr_dhcp.write('dhcp_relay,{},{}\n'.format(string_dhcp, string_vrf))
        else:
            wr_dhcp.write('dhcp_relay,{},default\n'.format(string_dhcp))
        line_count += 1
    elif re.search(re_desc, line):
        # Found a Description on the Interface
        string_desc = function_desc(line)
        line_count += 1
    elif line == "\n":
        # Found blank line, which means the end of the interface, time to create the output
        if not string_desc:
            string_desc = 'undefined'
        if not string_ipv4:
            line_count += 1
        elif string_ipv4:
            bd = function_vlan_to_bd(string_ivlan)
            check_ipv4 = ipaddress.IPv4Interface(string_ipv4)
            network_v4 = check_ipv4.network
            if string_hsrpv4:
                a,b = string_ipv4.split('/')
                gtwy = str(string_hsrpv4) + '/' + str(b)
            else:
                gtwy = str(string_ipv4)
            if string_vrf:
                wr_ivlan.write('subnet_add,primary,{},{},{},{}\n'.format(bd, gtwy, string_vrf, string_desc))
            else:
                wr_ivlan.write('subnet_add,primary,{},{},default,{}\n'.format(bd, gtwy, string_desc))
            if string_ipv4_sec:
                if string_hsrpv4_sec:
                    a,b = string_ipv4_sec.split('/')
                    gtwy = str(string_hsrpv4_sec) + '/' + str(b)
                else:
                    gtwy = str(string_ipv4)
                if string_vrf:
                    wr_ivlan.write('subnet_add,secondary,{},{},{},{}\n'.format(bd, gtwy, string_vrf, string_desc))
                else:
                    wr_ivlan.write('subnet_add,secondary,{},{},default,{}\n'.format(bd, gtwy, string_desc))
            line_count += 1
        
        # Reset the Variables back to Blank
        string_dhcp = ''
        string_desc = ''
        string_hsrpv4 = ''
        string_hsrpv4_sec = ''
        string_ipv4 = ''
        string_ipv4_sec = ''
        string_ivlan = ''
        string_vrf = ''
    else:
        line_count += 1


file.close()
wr_vlan.close()
wr_name.close()
wr_ivlan.close()
wr_dhcp.close()

#Get VLAN's that don't have a name and those that do and combine into one file
vlan_line_count = len(open('vlan_list.csv').readlines(  ))
bridge_list_1 = open('vlan_list.csv', 'r') 
bridge_list_2 = open('vlan_name.csv', 'r')
bridge_list_3 = open('vlan_comb.csv', 'w')
vlan_lines = bridge_list_1.readlines()
name_lines = bridge_list_2.readlines()
for lineg1 in vlan_lines:
    matched = 0
    lineg1 = lineg1.strip()
    for lineg2 in name_lines:
        lineg2 = lineg2.strip()
        if lineg1 in lineg2:
            matched +=1
    if matched == 0:
        bridge_list_3.write('{}\n'.format(lineg1))
        #print(x,y)
for line in name_lines:
    line.strip()
    bridge_list_3.write('{}'.format(line))

bridge_list_1.close()
bridge_list_2.close()
bridge_list_3.close()

#Sort the combined VLANs in final output file
bridge_list_3 = open('vlan_comb.csv', 'r')
bridge_list_4 = open('vlan_bddm.csv', 'w')
bridge_list_4.write('type,bd_type,Bridge_Domain,Description\n')
bddm = bridge_list_3.readlines()
bddm.sort()
for line in range(len(bddm)):
    bddm[line]
    bridge_list_4.write('bd_add,extend_out,{}'.format(bddm[line]))

bridge_list_3.close()
bridge_list_4.close()

dhcp_relay_uniq = 'cat dhcp.csv | sort | uniq > dhcp_sort.csv'
dhcp_relay_add_header = 'echo "type,Relay Address,VRF" | cat - dhcp_sort.csv > dhcp_relay.csv'
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