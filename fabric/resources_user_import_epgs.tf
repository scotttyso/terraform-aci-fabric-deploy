# This File will include EPGs

resource "aci_application_epg" "v0001_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v0001_epg"
	description            = "None"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v0001_bd.id
}

resource "aci_application_epg" "v0056_epg" {
	depends_on              = [aci_application_profile.dmz_nets]
	application_profile_dn = aci_application_profile.dmz_nets.id
	name                   = "v0056_epg"
	description            = "intersite-peering"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v0056_bd.id
}

resource "aci_application_epg" "v0064_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v0064_epg"
	description            = "OOBMgmt"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v0064_bd.id
}

resource "aci_application_epg" "v0080_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v0080_epg"
	description            = "Vlan80"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v0080_bd.id
}

resource "aci_application_epg" "v0087_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v0087_epg"
	description            = "markStephensLab"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v0087_bd.id
}

resource "aci_application_epg" "v0090_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v0090_epg"
	description            = "paulMerlittiLab"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v0090_bd.id
}

resource "aci_application_epg" "v0091_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v0091_epg"
	description            = "inBandMgmt"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v0091_bd.id
}

resource "aci_application_epg" "v0110_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v0110_epg"
	description            = "Wakanda-inband.L3Out"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v0110_bd.id
}

resource "aci_application_epg" "v0136_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v0136_epg"
	description            = "Asgard-inband.L3Out"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v0136_bd.id
}

resource "aci_application_epg" "v0168_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v0168_epg"
	description            = "Storage"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v0168_bd.id
}

resource "aci_application_epg" "v0169_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v0169_epg"
	description            = "Streched_vl811"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v0169_bd.id
}

resource "aci_application_epg" "v0691_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v0691_epg"
	description            = "Loki"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v0691_bd.id
}

resource "aci_application_epg" "v0811_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v0811_epg"
	description            = "GW1_Path1"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v0811_bd.id
}

resource "aci_application_epg" "v0812_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v0812_epg"
	description            = "GW1_Path2"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v0812_bd.id
}

resource "aci_application_epg" "v0995_epg" {
	depends_on              = [aci_application_profile.dmz_nets]
	application_profile_dn = aci_application_profile.dmz_nets.id
	name                   = "v0995_epg"
	description            = "coreL3Peer"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v0995_bd.id
}

resource "aci_application_epg" "v0996_epg" {
	depends_on              = [aci_application_profile.dmz_nets]
	application_profile_dn = aci_application_profile.dmz_nets.id
	name                   = "v0996_epg"
	description            = "inside"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v0996_bd.id
}

resource "aci_application_epg" "v0997_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v0997_epg"
	description            = "dirtyDMZ"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v0997_bd.id
}

resource "aci_application_epg" "v0998_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v0998_epg"
	description            = "None"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v0998_bd.id
}

resource "aci_application_epg" "v0999_epg" {
	depends_on              = [aci_application_profile.dmz_nets]
	application_profile_dn = aci_application_profile.dmz_nets.id
	name                   = "v0999_epg"
	description            = "ASE_Data"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v0999_bd.id
}

resource "aci_application_epg" "v3001_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v3001_epg"
	description            = "None"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v3001_bd.id
}

resource "aci_application_epg" "v3003_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v3003_epg"
	description            = "None"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v3003_bd.id
}

resource "aci_application_epg" "v3004_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v3004_epg"
	description            = "None"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v3004_bd.id
}

resource "aci_application_epg" "v3006_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v3006_epg"
	description            = "vMotion"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v3006_bd.id
}

resource "aci_application_epg" "v3007_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v3007_epg"
	description            = "east-common-tenant-l3"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v3007_bd.id
}

resource "aci_application_epg" "v3011_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v3011_epg"
	description            = "Asgard.Common.HNB.L3Out"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v3011_bd.id
}

resource "aci_application_epg" "v3019_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v3019_epg"
	description            = "Wakanda.Common.HNB.L3Out"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v3019_bd.id
}

resource "aci_application_epg" "v3103_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v3103_epg"
	description            = "Wakanda.Mercy.L3Out"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v3103_bd.id
}

resource "aci_application_epg" "v3910_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v3910_epg"
	description            = "Asgard.Mercy.L3Out"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v3910_bd.id
}

resource "aci_application_epg" "v3960_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v3960_epg"
	description            = "Wakanda.HNB.L3Out"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v3960_bd.id
}

resource "aci_application_epg" "v3961_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v3961_epg"
	description            = "Asgard.HNB.L3Out"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v3961_bd.id
}

resource "aci_application_epg" "v3962_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v3962_epg"
	description            = "Asgard_Common_L3Out"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v3962_bd.id
}

resource "aci_application_epg" "v3963_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v3963_epg"
	description            = "Asgard-Infra"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v3963_bd.id
}

resource "aci_application_epg" "v3964_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v3964_epg"
	description            = "Wakanda.HNB.L3Out"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v3964_bd.id
}

resource "aci_application_epg" "v3965_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v3965_epg"
	description            = "Asgard.HNB.L3Out"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v3965_bd.id
}

resource "aci_application_epg" "v3966_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v3966_epg"
	description            = "Asgard_Common_L3Out"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v3966_bd.id
}

resource "aci_application_epg" "v3967_epg" {
	depends_on              = [aci_application_profile.prod_nets]
	application_profile_dn = aci_application_profile.prod_nets.id
	name                   = "v3967_epg"
	description            = "Asgard-Infra"
	flood_on_encap         = "disabled"
	has_mcast_source       = "no"
	is_attr_based_epg      = "no"
	match_t                = "AtleastOne"
	pc_enf_pref            = "enforced"
	prio                   = "unspecified"
	shutdown               = "no"
	relation_fv_rs_bd      = aci_bridge_domain.v3967_bd.id
}

