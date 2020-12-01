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

resource "aci_any" "pref_group" {
	for_each		= var.user_vrfs_pg
	vrf_dn       	= "/uni/tn-${each.value.tenant}ctx-${each.value.vrf}"
	description  	= each.value.description
	pref_gr_memb 	= "enabled"
}

resource "aci_any" "vzAny" {
	for_each    				= var.user_vrfs_vzany
	vrf_dn       				= "/uni/tn-${each.value.tenant}ctx-${each.value.vrf}"
	description  				= each.value.description
	match_t      				= "AtleastOne"
	relation_vz_rs_any_to_cons	= "uni/tn-common/brc-default"
	relation_vz_rs_any_to_prov	= "uni/tn-common/brc-default"
}
