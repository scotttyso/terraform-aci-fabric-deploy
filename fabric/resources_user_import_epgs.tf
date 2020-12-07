# This File will include EPGs

resource "aci_application_epg" "dmz_nets_v0056_epg" {
	depends_on                     = [aci_application_profile.dmz_nets]
	application_profile_dn         = aci_application_profile.dmz_nets.id
	name                           = "v0056_epg"
	description                    = "intersite-peering"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "exclude"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v0056_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v0056_epg" {
	depends_on		= [aci_application_epg.dmz_nets_v0056_epg]
	path		= "/api/node/mo/uni/tn-dmz/ap-nets/epg-v0056_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "dmz_nets_v0995_epg" {
	depends_on                     = [aci_application_profile.dmz_nets]
	application_profile_dn         = aci_application_profile.dmz_nets.id
	name                           = "v0995_epg"
	description                    = "GW1_Path1"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "exclude"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v0995_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v0995_epg" {
	depends_on		= [aci_application_epg.dmz_nets_v0995_epg]
	path		= "/api/node/mo/uni/tn-dmz/ap-nets/epg-v0995_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "dmz_nets_v0996_epg" {
	depends_on                     = [aci_application_profile.dmz_nets]
	application_profile_dn         = aci_application_profile.dmz_nets.id
	name                           = "v0996_epg"
	description                    = "GW1_Path2"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "exclude"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v0996_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v0996_epg" {
	depends_on		= [aci_application_epg.dmz_nets_v0996_epg]
	path		= "/api/node/mo/uni/tn-dmz/ap-nets/epg-v0996_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "dmz_nets_v0999_epg" {
	depends_on                     = [aci_application_profile.dmz_nets]
	application_profile_dn         = aci_application_profile.dmz_nets.id
	name                           = "v0999_epg"
	description                    = "dirtyDMZ"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "exclude"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v0999_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v0999_epg" {
	depends_on		= [aci_application_epg.dmz_nets_v0999_epg]
	path		= "/api/node/mo/uni/tn-dmz/ap-nets/epg-v0999_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v0001_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v0001_epg"
	description                    = "None"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v0001_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v0001_epg" {
	depends_on		= [aci_application_epg.prod_nets_v0001_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v0001_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v0064_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v0064_epg"
	description                    = "OOBMgmt"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v0064_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v0064_epg" {
	depends_on		= [aci_application_epg.prod_nets_v0064_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v0064_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v0080_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v0080_epg"
	description                    = "Vlan80"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v0080_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v0080_epg" {
	depends_on		= [aci_application_epg.prod_nets_v0080_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v0080_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v0087_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v0087_epg"
	description                    = "None"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v0087_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v0087_epg" {
	depends_on		= [aci_application_epg.prod_nets_v0087_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v0087_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v0090_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v0090_epg"
	description                    = "markStephensLab"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v0090_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v0090_epg" {
	depends_on		= [aci_application_epg.prod_nets_v0090_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v0090_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v0091_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v0091_epg"
	description                    = "paulMerlittiLab"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v0091_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v0091_epg" {
	depends_on		= [aci_application_epg.prod_nets_v0091_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v0091_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v0110_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v0110_epg"
	description                    = "inBandMgmt"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v0110_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v0110_epg" {
	depends_on		= [aci_application_epg.prod_nets_v0110_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v0110_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v0136_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v0136_epg"
	description                    = "None"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v0136_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v0136_epg" {
	depends_on		= [aci_application_epg.prod_nets_v0136_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v0136_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v0168_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v0168_epg"
	description                    = "Wakanda-inband.L3Out"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v0168_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v0168_epg" {
	depends_on		= [aci_application_epg.prod_nets_v0168_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v0168_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v0169_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v0169_epg"
	description                    = "Asgard-inband.L3Out"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v0169_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v0169_epg" {
	depends_on		= [aci_application_epg.prod_nets_v0169_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v0169_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v0691_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v0691_epg"
	description                    = "Stprage"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v0691_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v0691_epg" {
	depends_on		= [aci_application_epg.prod_nets_v0691_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v0691_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v0811_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v0811_epg"
	description                    = "Stretched_vl811"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v0811_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v0811_epg" {
	depends_on		= [aci_application_epg.prod_nets_v0811_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v0811_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v0812_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v0812_epg"
	description                    = "Loki"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v0812_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v0812_epg" {
	depends_on		= [aci_application_epg.prod_nets_v0812_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v0812_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v0997_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v0997_epg"
	description                    = "coreL3Peer"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v0997_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v0997_epg" {
	depends_on		= [aci_application_epg.prod_nets_v0997_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v0997_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v0998_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v0998_epg"
	description                    = "coreL3Peer"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v0998_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v0998_epg" {
	depends_on		= [aci_application_epg.prod_nets_v0998_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v0998_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v3001_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v3001_epg"
	description                    = "inside"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v3001_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v3001_epg" {
	depends_on		= [aci_application_epg.prod_nets_v3001_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v3001_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v3003_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v3003_epg"
	description                    = "None"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v3003_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v3003_epg" {
	depends_on		= [aci_application_epg.prod_nets_v3003_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v3003_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v3004_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v3004_epg"
	description                    = "ASE_Data"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v3004_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v3004_epg" {
	depends_on		= [aci_application_epg.prod_nets_v3004_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v3004_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v3006_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v3006_epg"
	description                    = "None"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v3006_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v3006_epg" {
	depends_on		= [aci_application_epg.prod_nets_v3006_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v3006_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v3007_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v3007_epg"
	description                    = "None"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v3007_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v3007_epg" {
	depends_on		= [aci_application_epg.prod_nets_v3007_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v3007_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v3011_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v3011_epg"
	description                    = "None"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v3011_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v3011_epg" {
	depends_on		= [aci_application_epg.prod_nets_v3011_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v3011_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v3019_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v3019_epg"
	description                    = "None"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v3019_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v3019_epg" {
	depends_on		= [aci_application_epg.prod_nets_v3019_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v3019_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v3103_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v3103_epg"
	description                    = "vMotion"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v3103_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v3103_epg" {
	depends_on		= [aci_application_epg.prod_nets_v3103_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v3103_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v3910_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v3910_epg"
	description                    = "east-common-tenant-l3"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v3910_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v3910_epg" {
	depends_on		= [aci_application_epg.prod_nets_v3910_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v3910_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v3960_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v3960_epg"
	description                    = "Asgard.Common.HNB.L3Out"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v3960_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v3960_epg" {
	depends_on		= [aci_application_epg.prod_nets_v3960_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v3960_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v3961_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v3961_epg"
	description                    = "Wakanda.Common.HNB.L3Out"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v3961_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v3961_epg" {
	depends_on		= [aci_application_epg.prod_nets_v3961_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v3961_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v3962_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v3962_epg"
	description                    = "Wakanda.Mercy.L3Out"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v3962_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v3962_epg" {
	depends_on		= [aci_application_epg.prod_nets_v3962_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v3962_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v3963_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v3963_epg"
	description                    = "Asgard.Mercy.L3Out"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v3963_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v3963_epg" {
	depends_on		= [aci_application_epg.prod_nets_v3963_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v3963_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v3964_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v3964_epg"
	description                    = "Wakanda.HNB.L3Out"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v3964_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v3964_epg" {
	depends_on		= [aci_application_epg.prod_nets_v3964_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v3964_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v3965_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v3965_epg"
	description                    = "Asgard.HNB.L3Out"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v3965_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v3965_epg" {
	depends_on		= [aci_application_epg.prod_nets_v3965_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v3965_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v3966_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v3966_epg"
	description                    = "Asgard_Common_L3Out"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v3966_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v3966_epg" {
	depends_on		= [aci_application_epg.prod_nets_v3966_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v3966_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_nets_v3967_epg" {
	depends_on                     = [aci_application_profile.prod_nets]
	application_profile_dn         = aci_application_profile.prod_nets.id
	name                           = "v3967_epg"
	description                    = "Asgard-Infra"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "unspecified"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.v3967_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_v3967_epg" {
	depends_on		= [aci_application_epg.prod_nets_v3967_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-nets/epg-v3967_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_sap_app_sapapp_epg" {
	depends_on                     = [aci_application_profile.prod_sap_app]
	application_profile_dn         = aci_application_profile.prod_sap_app.id
	name                           = "sapapp_epg"
	description                    = "SAP HANA - Application Services"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "level3"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.sap_app_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_sapapp_epg" {
	depends_on		= [aci_application_epg.prod_sap_app_sapapp_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-sap_app/epg-sapapp_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_sap_db_sapdb_epg" {
	depends_on                     = [aci_application_profile.prod_sap_db]
	application_profile_dn         = aci_application_profile.prod_sap_db.id
	name                           = "sapdb_epg"
	description                    = "SAP HANA - Database Services"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "level3"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.sap_db_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_sapdb_epg" {
	depends_on		= [aci_application_epg.prod_sap_db_sapdb_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-sap_db/epg-sapdb_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_sap_intg_sapsda_epg" {
	depends_on                     = [aci_application_profile.prod_sap_intg]
	application_profile_dn         = aci_application_profile.prod_sap_intg.id
	name                           = "sapsda_epg"
	description                    = "SAP HANA - Smart Data Access"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "level3"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.sap_itg_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_sapsda_epg" {
	depends_on		= [aci_application_epg.prod_sap_intg_sapsda_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-sap_intg/epg-sapsda_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_sap_intg_sapsdi_epg" {
	depends_on                     = [aci_application_profile.prod_sap_intg]
	application_profile_dn         = aci_application_profile.prod_sap_intg.id
	name                           = "sapsdi_epg"
	description                    = "SAP HANA - Smart Data Integration"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "level3"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.sap_itg_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_sapsdi_epg" {
	depends_on		= [aci_application_epg.prod_sap_intg_sapsdi_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-sap_intg/epg-sapsdi_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_sap_intg_sapsds_epg" {
	depends_on                     = [aci_application_profile.prod_sap_intg]
	application_profile_dn         = aci_application_profile.prod_sap_intg.id
	name                           = "sapsds_epg"
	description                    = "SAP HANA - Smart Data Streaming (CEP)"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "level3"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.sap_itg_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_sapsds_epg" {
	depends_on		= [aci_application_epg.prod_sap_intg_sapsds_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-sap_intg/epg-sapsds_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_sap_intg_saprds_epg" {
	depends_on                     = [aci_application_profile.prod_sap_intg]
	application_profile_dn         = aci_application_profile.prod_sap_intg.id
	name                           = "saprds_epg"
	description                    = "SAP HANA - Remote Data Sync"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "level3"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.sap_itg_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_saprds_epg" {
	depends_on		= [aci_application_epg.prod_sap_intg_saprds_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-sap_intg/epg-saprds_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

resource "aci_application_epg" "prod_sap_intg_saphdi_epg" {
	depends_on                     = [aci_application_profile.prod_sap_intg]
	application_profile_dn         = aci_application_profile.prod_sap_intg.id
	name                           = "saphdi_epg"
	description                    = "SAP HANA - Hadoop Integration"
	flood_on_encap                 = "disabled"
	has_mcast_source               = "no"
	is_attr_based_epg              = "no"
	match_t                        = "AtleastOne"
	pc_enf_pref                    = "enforced"
	pref_gr_memb                   = "include"
	prio                           = "level3"
	shutdown                       = "no"
	relation_fv_rs_bd              = aci_bridge_domain.sap_itg_bd.id
	relation_fv_rs_aepg_mon_pol    = "uni/tn-common/monepg-default"
}

resource "aci_rest" "phys-access_phys_to_saphdi_epg" {
	depends_on		= [aci_application_epg.prod_sap_intg_saphdi_epg]
	path		= "/api/node/mo/uni/tn-prod/ap-sap_intg/epg-saphdi_epg.json"
	class_name	= "fvRsDomAtt"
	payload		= <<EOF
{
    "fvRsDomAtt": {
        "attributes": {
            "tDn": "uni/phys-access_phys"
        },
        "children": []
    }
}
	EOF
}

