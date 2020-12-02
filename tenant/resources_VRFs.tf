resource "aci_vrf" "default" {
	for_each    						= var.user_vrfs
	tenant_dn							= "/uni/tn-${each.value.tenant}"
	name        						= each.value.name
	bd_enforced_enable					= "enabled"
	ip_data_plane_learning				= "enabled"
	pc_enf_pref							= "enforced"
	pc_enf_dir							= "ingress"
	relation_fv_rs_ctx_mon_pol			= "/uni/tn-common/monepg-default"
	relation_fv_rs_ctx_to_ep_ret		= "/uni/tn-common/epRPol-default"
	relation_fv_rs_vrf_validation_pol	= "/uni/tn-common/vrfvalidationpol-default"
}

