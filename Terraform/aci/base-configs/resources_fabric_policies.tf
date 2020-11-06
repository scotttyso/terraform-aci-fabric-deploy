resource "aci_attachable_access_entity_profile" "default" {
	for_each    = var.aep_policies
	description = each.value.description
	name        = each.value.name
}

resource "aci_cdp_interface_policy" "default" {
	for_each    = var.cdp_policies
	name        = each.value.name
	admin_st    = each.value.admin_st
}

resource "aci_fabric_if_pol" "default" {
	for_each    = var.interface_policies
	name        = each.value.name
	description = each.value.description
	auto_neg    = each.value.auto_neg
	speed       = each.value.speed
}

resource "aci_firmware_group" "default" {
	for_each   			= var.fwg_policies
	name       			= each.value.name
	firmware_group_type = each.value.firmware_group_type
}

resource "aci_interface_fc_policy" "default" {
	for_each    = var.int_fc_policies
	name        = each.value.name
	port_mode	= each.value.port_mode
	speed		= each.value.speed
	trunk_mode  = each.value.trunk_mode
}

resource "aci_l3_domain_profile" "default" {
	for_each    = var.l3dom_profile
	name        = each.value.name
}

resource "aci_lacp_policy" "default" {
	for_each    = var.lacp_policies
	description = each.value.description
	name        = each.value.name
	mode        = each.value.mode
}

resource "aci_lldp_interface_policy" "default" {
	for_each    = var.lldp_policies
	description = each.value.description
	name        = each.value.name
	admin_rx_st = each.value.admin_rx_st
	admin_tx_st = each.value.admin_tx_st
}

resource "aci_miscabling_protocol_interface_policy" "default" {
	for_each    = var.mcp_policies
	description = each.value.description
	name        = each.value.name
	admin_st    = each.value.admin_st
}

resource "aci_physical_domain" "default" {
	for_each    = var.physical_domain
	name        = each.value.name
}

resource "aci_vlan_pool" "default" {
	for_each    = var.vlan_pool
	name        = each.value.name
	alloc_mode  = each.value.alloc_mode
}

resource "aci_ranges" "default" {
  vlan_pool_dn	= "uni/infra/vlanns-[msite.vl-pool]-static"
  _from		= "vlan-4"
  to		= "vlan-4"
}
