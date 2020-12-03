# This File will include VRFs

resource "aci_vrf" "prod_vrf" {
	tenant_dn							= "uni/tn-common"
	name        						= "prod_vrf"
	bd_enforced_enable				    = "yes"
	ip_data_plane_learning			    = "enabled"
	pc_enf_pref						    = "enforced"
	pc_enf_dir						    = "ingress"
	relation_fv_rs_ctx_mon_pol		    = "uni/tn-common/monepg-default"
	relation_fv_rs_ctx_to_ep_ret		= "uni/tn-common/epRPol-default"
	relation_fv_rs_vrf_validation_pol	= "uni/tn-common/vrfvalidationpol-default"
}

resource "aci_any" "prod_vrf_pc" {
	vrf_dn 				        = "uni/tn-common/ctx-prod_vrf"
	description 				= "Prod_vrf description"
	pref_gr_memb                = "enabled"
}

resource "aci_vrf" "dmz_vrf" {
	tenant_dn							= "uni/tn-common"
	name        						= "dmz_vrf"
	bd_enforced_enable				    = "yes"
	ip_data_plane_learning			    = "enabled"
	pc_enf_pref						    = "enforced"
	pc_enf_dir						    = "ingress"
	relation_fv_rs_ctx_mon_pol		    = "uni/tn-common/monepg-default"
	relation_fv_rs_ctx_to_ep_ret		= "uni/tn-common/epRPol-default"
	relation_fv_rs_vrf_validation_pol	= "uni/tn-common/vrfvalidationpol-default"
}

resource "aci_any" "dmz_vrf_pc" {
	vrf_dn 				        = "uni/tn-common/ctx-dmz_vrf"
	description 				= "None"
	match_t      				= "AtleastOne"
}

resource "aci_rest" "vzAny_dmz_vrf_Cons" {
	path		= "/api/node/mo/uni/tn-common/ctx-dmz_vrf/any.json"
	class_name	= "vzRsAnyToCons"
	payload		= <<EOF
{
    "vzRsAnyToCons": {
        "attributes": {
            "tnVzBrCPName": "default"
        }
    }
}
	EOF
}

resource "aci_rest" "vzAny_dmz_vrf_Prov" {
	path		= "/api/node/mo/uni/tn-common/ctx-dmz_vrf/any.json"
	class_name	= "vzRsAnyToProv"
	payload		= <<EOF
{
    "vzRsAnyToProv": {
        "attributes": {
            "tnVzBrCPName": "default"
        }
    }
}
	EOF
}

resource "aci_vrf" "Prod1_vrf" {
	tenant_dn							= "uni/tn-common"
	name        						= "Prod1_vrf"
	bd_enforced_enable				    = "yes"
	ip_data_plane_learning			    = "enabled"
	pc_enf_pref						    = "enforced"
	pc_enf_dir						    = "ingress"
	relation_fv_rs_ctx_mon_pol		    = "uni/tn-common/monepg-default"
	relation_fv_rs_ctx_to_ep_ret		= "uni/tn-common/epRPol-default"
	relation_fv_rs_vrf_validation_pol	= "uni/tn-common/vrfvalidationpol-default"
}

resource "aci_any" "Prod1_vrf_pc" {
	vrf_dn 				        = "uni/tn-common/ctx-Prod1_vrf"
	description 				= "vrf1 description"
	pref_gr_memb                = "enabled"
}

resource "aci_vrf" "Prod2_vrf" {
	tenant_dn							= "uni/tn-common"
	name        						= "Prod2_vrf"
	bd_enforced_enable				    = "yes"
	ip_data_plane_learning			    = "enabled"
	pc_enf_pref						    = "enforced"
	pc_enf_dir						    = "ingress"
	relation_fv_rs_ctx_mon_pol		    = "uni/tn-common/monepg-default"
	relation_fv_rs_ctx_to_ep_ret		= "uni/tn-common/epRPol-default"
	relation_fv_rs_vrf_validation_pol	= "uni/tn-common/vrfvalidationpol-default"
}

resource "aci_any" "Prod2_vrf_pc" {
	vrf_dn 				        = "uni/tn-common/ctx-Prod2_vrf"
	description 				= "vrf2 description"
	match_t      				= "AtleastOne"
}

resource "aci_rest" "vzAny_Prod2_vrf_Cons" {
	path		= "/api/node/mo/uni/tn-common/ctx-Prod2_vrf/any.json"
	class_name	= "vzRsAnyToCons"
	payload		= <<EOF
{
    "vzRsAnyToCons": {
        "attributes": {
            "tnVzBrCPName": "default"
        }
    }
}
	EOF
}

resource "aci_rest" "vzAny_Prod2_vrf_Prov" {
	path		= "/api/node/mo/uni/tn-common/ctx-Prod2_vrf/any.json"
	class_name	= "vzRsAnyToProv"
	payload		= <<EOF
{
    "vzRsAnyToProv": {
        "attributes": {
            "tnVzBrCPName": "default"
        }
    }
}
	EOF
}

