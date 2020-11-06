
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
