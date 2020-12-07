# This File will include VRFs

resource "aci_vrf" "prod_vrf" {
	tenant_dn                           = "uni/tn-common"
	name                                = "prod_vrf"
	bd_enforced_enable                  = "yes"
	ip_data_plane_learning			    = "enabled"
	pc_enf_pref						    = "enforced"
	pc_enf_dir						    = "ingress"
	relation_fv_rs_ctx_mon_pol		    = "uni/tn-common/monepg-default"
	relation_fv_rs_ctx_to_ep_ret		= "uni/tn-common/epRPol-default"
	relation_fv_rs_vrf_validation_pol   = "uni/tn-common/vrfvalidationpol-default"
}

resource "aci_any" "prod_vrf_any" {
	depends_on                     = [aci_vrf.prod_vrf]
	vrf_dn                         = "uni/tn-common/ctx-prod_vrf"
	description                    = "Product Tenant"
	pref_gr_memb  				   = "enabled"
}

resource "aci_vrf" "dmz_vrf" {
	tenant_dn                           = "uni/tn-common"
	name                                = "dmz_vrf"
	bd_enforced_enable                  = "yes"
	ip_data_plane_learning			    = "enabled"
	pc_enf_pref						    = "enforced"
	pc_enf_dir						    = "ingress"
	relation_fv_rs_ctx_mon_pol		    = "uni/tn-common/monepg-default"
	relation_fv_rs_ctx_to_ep_ret		= "uni/tn-common/epRPol-default"
	relation_fv_rs_vrf_validation_pol   = "uni/tn-common/vrfvalidationpol-default"
}

resource "aci_any" "dmz_vrf_any" {
	depends_on                     = [aci_vrf.dmz_vrf]
	vrf_dn                         = "uni/tn-common/ctx-dmz_vrf"
	description                    = "DMZ Tenant"
	match_t      				   = "AtleastOne"
}

