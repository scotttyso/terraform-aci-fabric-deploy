# Use this Resource File to Register spine101 with node id 101 to the Fabric
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

resource "aci_fabric_node_member" "spine101" {
	serial    = "TEP-1-103"
	name      = "spine101"
	node_id   = "101"
	node_type = "unspecified"
	role      = "spine"
	pod_id    = "1"
}

resource "aci_rest" "inband_mgmt_spine101" {
	path       = "/api/node/mo/uni/tn-mgmt"
	class_name = "mgmtRsOoBStNode"
	payload    = <<EOF
{
	"mgmtRsOoBStNode": {
		"attributes": {
			"addr":"192.168.89.13/24",
			"dn":"uni/tn-mgmt/mgmtp-default/oob-default/rsooBStNode-[topology/pod-'1'/node-101]",
			"gw":"192.168.89.1",
			"tDn":"topology/pod-'1'/node-101",
			"v6Addr":"::",
			"v6Gw":"::"
		}
	}
}
	EOF
}

resource "aci_rest" "inband_mgmt_spine101" {
	path       = "/api/node/mo/uni/tn-mgmt"
	class_name = "mgmtRsInBStNode"
	payload    = <<EOF
{
	"mgmtRsInBStNode": {
		"attributes": {
			"addr":"192.168.88.13/24",
			"dn":"uni/tn-mgmt/mgmtp-default/inb-inband_epg/rsinBStNode-[[topology/pod-'1'/node-101]",
			"gw":"192.168.88.1",
			"tDn":"topology/pod-'1'/node-101",
		}
	}
}
	EOF
}

