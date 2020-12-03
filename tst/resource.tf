resource "aci_leaf_interface_profile" "leaf203" {
	name	= "leaf203"
}

resource "aci_leaf_profile" "leaf203" {
  name  = "leaf203"
  relation_infra_rs_acc_port_p   = [aci_leaf_interface_profile.leaf203.id]
  leaf_selector {
    name    = "leaf203"
    switch_association_type = "range"
    node_block {
      name  = "leaf203"
      from_ = "203"
      to_   = "203"
    }
  }
}

resource "aci_access_port_selector" "leaf203" {
  leaf_interface_profile_dn  = aci_leaf_interface_profile.leaf203.id
  name                       = "Eth1-01"
  access_port_selector_type  = "range"
}

resource "aci_access_port_block" "leaf203" {
	access_port_selector_dn    = aci_access_port_selector.leaf203.id
	description                = "testing"
	name                       = "Eth1-01"
	from_card                  = "1"
	from_port                  = "1"
	to_card                    = "1"
	to_port                    = "1"
}