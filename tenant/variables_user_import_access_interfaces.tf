# This File will include Access Interfaces

resource "aci_leaf_access_port_policy_group" "access_host_apg" {
	description 				       = "143c-lab-gw1-Te0/0/4"
	name 						       = "access_host_apg"
	relation_infra_rs_att_ent_p	       = "uni/infra/attentp-access_aep"
	relation_infra_rs_cdp_if_pol       = "uni/infra/cdpIfP-cdp_Enabled"
	relation_infra_rs_h_if_pol	       = "uni/infra/hintfpol-inherit_Auto"
	relation_infra_rs_lldp_if_pol      = "uni/infra/lldpIfP-lldp_Enabled"
	relation_infra_rs_mcp_if_pol       = "uni/infra/mcpIfP-mcp_Enabled"
	relation_infra_rs_mon_if_infra_pol = "uni/infra/moninfra-default"
	relation_infra_rs_stp_if_pol       = "uni/infra/ifPol-no"
}

