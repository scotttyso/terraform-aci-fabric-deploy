# This File will include DNS, Domain, NTP, Timezone and other base configuration parameters
resource "aci_rest" "bgp_as" {
	path       = "/api/node/mo/uni/fabric/bgpInstP-default/as.json"
	class_name = "bgpAsP"
	payload    = <<EOF
{
	"bgpAsP": {
		"attributes": {
			"dn": "uni/fabric/bgpInstP-default/as",
			"asn": "65535",
			"rn": "as"
		}
	}
}
	EOF
}

resource "aci_rest" "bgp_rr_101" {
	path       = "/api/node/mo/uni/fabric/bgpInstP-default/rr/node-101.json"
	class_name = "bgpRRNodePEp"
	payload    = <<EOF
{
	"bgpRRNodePEp": {
		"attributes": {
			"dn": "uni/fabric/bgpInstP-default/rr/node-101",
			"id": "101",
			"rn": "node-101"
		}
	}
}
	EOF
}

resource "aci_rest" "dns_mgmt" {
	path       = "/api/node/mo/uni/fabric/dnsp-default.json"
	class_name = "dnsRsProfileToEpg"
	payload    = <<EOF
{
	"dnsRsProfileToEpg": {
		"attributes": {
			"tDn": "uni/tn-mgmt/mgmtp-default/oob-default",
		}
	}
}
	EOF
}

resource "aci_rest" "dns_10_101_128_15" {
	path       = "api/node/mo/uni/fabric/dnsp-default/prov-[10.101.128.15].json"
	class_name = "dnsProv"
	payload    = <<EOF
{
	"dnsProv": {
		"attributes": {
			"dn": "uni/fabric/dnsp-default/prov-[10.101.128.15]",
			"addr": "10.101.128.15",
			"preferred": "no",
			"rn": "prov-[10.101.128.15]"
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "dns_10_101_128_16" {
	path       = "api/node/mo/uni/fabric/dnsp-default/prov-[10.101.128.16].json"
	class_name = "dnsProv"
	payload    = <<EOF
{
	"dnsProv": {
		"attributes": {
			"dn": "uni/fabric/dnsp-default/prov-[10.101.128.16]",
			"addr": "10.101.128.16",
			"preferred": "yes",
			"rn": "prov-[10.101.128.16]"
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "ntp_192_168_64_39" {
	path       = "/api/node/mo/uni/fabric/time-default/ntpprov-192.168.64.39.json"
	class_name = "datetimeNtpProv"
	payload    = <<EOF
{
	"datetimeNtpProv": {
		"attributes": {
			"dn": "uni/fabric/time-default/ntpprov-192.168.64.39",
			"name": "192.168.64.39",
			"preferred": "true",
			"rn": "ntpprov-192.168.64.39",
		},
		"children": [
			{
				"datetimeRsNtpProvToEpg": {
					"attributes": {
						"tDn": "uni/tn-mgmt/mgmtp-default/oob-default",
					}
				}
			}
		]
	}
}
	EOF
}

resource "aci_rest" "ntp_10_101_128_15" {
	path       = "/api/node/mo/uni/fabric/time-default/ntpprov-10.101.128.15.json"
	class_name = "datetimeNtpProv"
	payload    = <<EOF
{
	"datetimeNtpProv": {
		"attributes": {
			"dn": "uni/fabric/time-default/ntpprov-10.101.128.15",
			"name": "10.101.128.15",
			"preferred": "false",
			"rn": "ntpprov-10.101.128.15",
		},
		"children": [
			{
				"datetimeRsNtpProvToEpg": {
					"attributes": {
						"tDn": "uni/tn-mgmt/mgmtp-default/oob-default",
					}
				}
			}
		]
	}
}
	EOF
}

resource "aci_rest" "domain_rich_ciscolabs_com" {
	path       = "api/node/mo/uni/fabric/dnsp-default/dom-[rich.ciscolabs.com].json"
	class_name = "dnsDomain"
	payload    = <<EOF
{
	"dnsDomain": {
		"attributes": {
			"dn": "uni/fabric/dnsp-default/dom-[rich.ciscolabs.com]",
			"name": "rich.ciscolabs.com",
			"isDefault": "yes",
			"rn": "dom-[rich.ciscolabs.com]"
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "snmp_client_10_0_0_1" {
	path       = "/api/node/mo/uni/fabric/snmppol-default/clgrp-Out-of-Band_Clients/client-[10.0.0.1].json"
	class_name = "snmpClientP"
	payload    = <<EOF
{
	"snmpClientP": {
		"attributes": {
			"dn": "uni/fabric/snmppol-default/clgrp-Out-of-Band_Clients/client-[10.0.0.1]",
			"name": "snmp-server1",
			"addr": "10.0.0.1",
			"rn": "client-10.0.0.1",
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "snmp_client_10_0_0_2" {
	path       = "/api/node/mo/uni/fabric/snmppol-default/clgrp-Inband_Clients/client-[10.0.0.2].json"
	class_name = "snmpClientP"
	payload    = <<EOF
{
	"snmpClientP": {
		"attributes": {
			"dn": "uni/fabric/snmppol-default/clgrp-Inband_Clients/client-[10.0.0.2]",
			"name": "snmp-server2",
			"addr": "10.0.0.2",
			"rn": "client-10.0.0.2",
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "snmp_info" {
	path       = "/api/node/mo/uni/fabric/snmppol-default.json"
	class_name = "snmpPol"
	payload    = <<EOF
{
	"snmpPol": {
		"attributes": {
			"dn": "uni/fabric/snmppol-default",
			"descr": "This is the default SNMP Policy",
			"adminSt": "enabled",
			"contact": "rich-lab@cisco.com",
			"loc": "Richfield Ohio",
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "snmp_comm_read_access" {
	path       = "/api/node/mo/uni/fabric/snmppol-default/community-read_access.json"
	class_name = "snmpCommunityP"
	payload    = <<EOF
{
	"snmpCommunityP": {
		"attributes": {
			"dn": "uni/fabric/snmppol-default/community-read_access",
			"descr": "is it needed",
			"name": "read_access",
			"rn": "community-read_access"
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "snmp_comm_will-this-work" {
	path       = "/api/node/mo/uni/fabric/snmppol-default/community-will-this-work.json"
	class_name = "snmpCommunityP"
	payload    = <<EOF
{
	"snmpCommunityP": {
		"attributes": {
			"dn": "uni/fabric/snmppol-default/community-will-this-work",
			"descr": "",
			"name": "will-this-work",
			"rn": "community-will-this-work"
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "snmp_user_cisco_user1" {
	path       = "/api/node/mo/uni/fabric/snmppol-default/user-cisco_user1.json"
	class_name = "snmpUserP"
	payload    = <<EOF
{
	"snmpUserP": {
		"attributes": {
			"privType": "aes-128",
			"privKey": "cisco123",
			"authKey": "cisco123",
			"authType": "hmac-sha1-96",
			"name": "cisco_user1",
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "snmp_user_cisco_user2" {
	path       = "/api/node/mo/uni/fabric/snmppol-default/user-cisco_user2.json"
	class_name = "snmpUserP"
	payload    = <<EOF
{
	"snmpUserP": {
		"attributes": {
			"privType": "des",
			"privKey": "cisco123",
			"authKey": "cisco123",
			"name": "cisco_user2",
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "snmp_user_cisco_user3" {
	path       = "/api/node/mo/uni/fabric/snmppol-default/user-cisco_user3.json"
	class_name = "snmpUserP"
	payload    = <<EOF
{
	"snmpUserP": {
		"attributes": {
			"authKey": "cisco123",
			"authType": "hmac-sha1-96",
			"name": "cisco_user3",
		},
		"children": []
	}
}
	EOF
}

