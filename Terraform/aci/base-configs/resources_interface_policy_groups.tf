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

