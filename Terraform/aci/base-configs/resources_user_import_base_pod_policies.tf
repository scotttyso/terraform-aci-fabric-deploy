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

