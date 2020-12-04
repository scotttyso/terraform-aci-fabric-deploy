resource "aci_ranges" "vlan_pool_add_995" {
	vlan_pool_dn   = "uni/infra/vlanns-[access_vl-pool]-static"
	_from          = "vlan-995"
	to		       = "vlan-995"
}

resource "aci_ranges" "vlan_pool_add_691" {
	vlan_pool_dn   = "uni/infra/vlanns-[access_vl-pool]-static"
	_from          = "vlan-691"
	to		       = "vlan-691"
}

