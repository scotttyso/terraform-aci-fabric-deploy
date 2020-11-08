# Use this Resource File to Register leaf201 with node id 201 to the Fabric
# Requirements are:
# serial: Actual Serial Number of the switch.
# name: Hostname you want to assign.
# node_id: unique ID used to identify the switch in the APIC.
#   in the "Cisco ACI Object Naming and Numbering: Best Practice
#   The recommendation is that the Spines should be 101-199
#   and leafs should start at 200+ thru 4000.  As the number of
#   spines should always be less than the number of leafs
# node_type: uremote-leaf-wan or unspecified.
# role: spine, leaf, or unspecified.
# pod_id: Typically this will be one unless you are running multipod.

resource "aci_fabric_node_member" "leaf201" {
	serial    = "TEP-1-101"
	name      = "leaf201"
	node_id   = "201"
	node_type = "unspecified"
	role      = "leaf"
	pod_id    = "1"
}

resource "aci_rest" "oob_mgmt_leaf201" {
	path       = "/api/node/mo/uni/tn-mgmt"
	class_name = "mgmtRsOoBStNode"
	payload    = <<EOF
{
	"mgmtRsOoBStNode": {
		"attributes": {
			"addr":"192.168.87.11/24",
			"dn":"uni/tn-mgmt/mgmtp-default/oob-default/rsooBStNode-[topology/pod-'1'/node-201]",
			"gw":"192.168.87.1",
			"tDn":"topology/pod-'1'/node-201",
			"v6Addr":"::",
			"v6Gw":"::"
		}
	}
}
	EOF
}

resource "aci_rest" "inband_mgmt_leaf201" {
	path       = "/api/node/mo/uni/tn-mgmt"
	class_name = "mgmtRsInBStNode"
	payload    = <<EOF
{
	"mgmtRsInBStNode": {
		"attributes": {
			"addr":"192.168.86.11/24",
			"dn":"uni/tn-mgmt/mgmtp-default/inb-inband_epg/rsinBStNode-[[topology/pod-'1'/node-201]",
			"gw":"192.168.86.1",
			"tDn":"topology/pod-'1'/node-201",
		}
	}
}
	EOF
}

resource "aci_leaf_profile" "leaf201" {
	name = "leaf201"
	leaf_selector {
		name                    = "leaf201"
		switch_association_type = "range"
		node_block {
			name  = "leaf201"
			from_ = "201"
			to_   = "201"
		}
	}
}

resource "aci_leaf_interface_profile" "leaf201" {
	name = "leaf201"
}

resource "aci_rest" "leaf_int_selector_leaf201" {
	path       = "/api/node/mo/uni/infra/nprof-leaf201.json"
	class_name = "infraRsAccPortP"
	payload    = <<EOF
{
	"infraRsAccPortP": {
		"attributes": {
			"tDn": "uni/infra/accportprof-leaf201"
		}
	}
}
	EOF
}

resource "aci_access_port_selector" "leaf201" {
	for_each                  = var.port_selector_48
	leaf_interface_profile_dn = aci_leaf_interface_profile.leaf201.id
	name                      = each.value.name
	access_port_selector_type = "range"
}

