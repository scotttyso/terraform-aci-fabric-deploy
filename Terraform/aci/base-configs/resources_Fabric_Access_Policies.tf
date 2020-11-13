resource "aci_attachable_access_entity_profile" "default" {
	for_each    = var.policies_aep
	description = each.value.description
	name        = each.value.name
}

resource "aci_cdp_interface_policy" "default" {
	for_each    = var.policies_cdp
	name        = each.value.name
	admin_st    = each.value.admin_st
}

resource "aci_fabric_if_pol" "default" {
	for_each    = var.policies_link_level
	name        = each.value.name
	description = each.value.description
	auto_neg    = each.value.auto_neg
	speed       = each.value.speed
}

resource "aci_interface_fc_policy" "default" {
	for_each    = var.policies_int_fc
	name        = each.value.name
	port_mode	= each.value.port_mode
	speed		= each.value.speed
	trunk_mode  = each.value.trunk_mode
}

resource "aci_lacp_policy" "default" {
	for_each    = var.policies_lacp
	description = each.value.description
	name        = each.value.name
	mode        = each.value.mode
}

resource "aci_lldp_interface_policy" "default" {
	for_each    = var.policies_lldp
	description = each.value.description
	name        = each.value.name
	admin_rx_st = each.value.admin_rx_st
	admin_tx_st = each.value.admin_tx_st
}

resource "aci_miscabling_protocol_interface_policy" "default" {
	for_each    = var.policies_mcp
	description = each.value.description
	name        = each.value.name
	admin_st    = each.value.admin_st
}

resource "aci_vlan_pool" "default" {
	for_each    = var.vlan_pool
	name        = each.value.name
	alloc_mode  = each.value.alloc_mode
}

resource "aci_l3_domain_profile" "default" {
	for_each    			  = var.profile_l3dom
	name        			  = each.value.name
	relation_infra_rs_vlan_ns = "uni/infra/vlanns-[${each.value.vl_pool}]-static"
}

resource "aci_physical_domain" "default" {
	for_each    = var.profile_physdom
	name        = each.value.name
	relation_infra_rs_vlan_ns = "uni/infra/vlanns-[${each.value.vl_pool}]-static"
}

resource "aci_ranges" "default" {
  vlan_pool_dn	= "uni/infra/vlanns-[msite_vl-pool]-static"
  _from		= "vlan-4"
  to		= "vlan-4"
}

resource "aci_rest" "stp-policies" {
	for_each   = var.policies_stp
	path       = "/api/node/mo/uni/infra/ifPol-${each.value.name}.json"
	class_name = "stpIfPol"
	payload    = <<EOF
{
	"stpIfPol": {
		"attributes": {
			"dn": "uni/infra/ifPol-${each.value.name}",
			"name": "${each.value.name}",
			"ctrl": "${each.value.ctrl}",
		},
	}
}
	EOF
}

resource "aci_leaf_access_port_policy_group" "inband_ap" {
	description 				  = "Inband port-group policy"
	name 						  = "inband_ap"
	relation_infra_rs_h_if_pol	  = "uni/infra/hintfpol-inherit_Auto"
	relation_infra_rs_mcp_if_pol  = "uni/infra/mcpIfP-mcp_Enabled"
	relation_infra_rs_lldp_if_pol = "uni/infra/lldpIfP-lldp_Enabled"
    relation_infra_rs_stp_if_pol  = "uni/infra/ifPol-BPDU_fg"
	relation_infra_rs_att_ent_p	  = "uni/infra/attentp-access_aep"
}

resource "aci_leaf_access_port_policy_group" "access_host_ap" {
	description 				  = "Template for a Host Access Port"
	name 						  = "access_host_ap"
	relation_infra_rs_h_if_pol	  = "uni/infra/hintfpol-inherit_Auto"
	relation_infra_rs_cdp_if_pol  = "uni/infra/cdpIfP-cdp_Disabled"
	relation_infra_rs_mcp_if_pol  = "uni/infra/mcpIfP-mcp_Enabled"
	relation_infra_rs_lldp_if_pol = "uni/infra/lldpIfP-lldp_Enabled"
    relation_infra_rs_stp_if_pol  = "uni/infra/ifPol-BPDU_fg"
	relation_infra_rs_att_ent_p	  = "uni/infra/attentp-access_aep"
}