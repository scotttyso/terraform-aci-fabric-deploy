# Use this Resource File to Register Nodes to the Fabric
# Variables are:
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

resource "aci_fabric_node_member" "sw101" {
	serial = "TEP-1-101"
	name = "sw101"
	node_id = "101"
	node_type = "unspecified"
	role = "unspecified"
	pod_id = "1"
}

resource "aci_fabric_node_member" "sw102" {
	serial = "TEP-1-102"
	name = "sw102"
	node_id = "102"
	node_type = "unspecified"
	role = "unspecified"
	pod_id = "1"
}

resource "aci_fabric_node_member" "sw103" {
	serial = "TEP-1-103"
	name = "sw103"
	node_id = "103"
	node_type = "unspecified"
	role = "unspecified"
	pod_id = "1"
}
