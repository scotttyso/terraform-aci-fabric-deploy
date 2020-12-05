# This File will include Port Group Confgiuration and Mapping

resource "aci_rest" "leaf201_Eth1-01_pg" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf201/hports-Eth1-01-typ-range/rsaccBaseGrp.json"
	class_name	= "infraRsAccBaseGrp"
	payload		= <<EOF
{
    "infraRsAccBaseGrp": {
        "attributes": {
            "tDn": "uni/infra/funcprof/brkoutportgrp-4x10g_pg"
        },
        "children": []
    }
}
	EOF
}

resource "aci_access_port_selector" "leaf201_Eth1-01-0" {
	leaf_interface_profile_dn  = aci_leaf_interface_profile.leaf201.id
	description                = "None"
	name                       = "Eth1-01-0"
	access_port_selector_type  = "range"
}

resource "aci_access_sub_port_block" "leaf201_Eth1-01-0" {
	depends_on                 = [aci_leaf_interface_profile.leaf201]
	access_port_selector_dn    = aci_access_port_selector.leaf201_Eth1-01-0.id
	name                       = "block0"
	from_card                  = "1"
	from_port                  = "1"
	from_sub_port              = "0"
	to_card                    = "1"
	to_port                    = "1"
	to_sub_port                = "0"
}

resource "aci_access_port_selector" "leaf201_Eth1-01-1" {
	leaf_interface_profile_dn  = aci_leaf_interface_profile.leaf201.id
	description                = "None"
	name                       = "Eth1-01-1"
	access_port_selector_type  = "range"
}

resource "aci_access_sub_port_block" "leaf201_Eth1-01-1" {
	depends_on                 = [aci_leaf_interface_profile.leaf201]
	access_port_selector_dn    = aci_access_port_selector.leaf201_Eth1-01-1.id
	name                       = "block1"
	from_card                  = "1"
	from_port                  = "1"
	from_sub_port              = "1"
	to_card                    = "1"
	to_port                    = "1"
	to_sub_port                = "1"
}

resource "aci_access_port_selector" "leaf201_Eth1-01-2" {
	leaf_interface_profile_dn  = aci_leaf_interface_profile.leaf201.id
	description                = "None"
	name                       = "Eth1-01-2"
	access_port_selector_type  = "range"
}

resource "aci_access_sub_port_block" "leaf201_Eth1-01-2" {
	depends_on                 = [aci_leaf_interface_profile.leaf201]
	access_port_selector_dn    = aci_access_port_selector.leaf201_Eth1-01-2.id
	name                       = "block2"
	from_card                  = "1"
	from_port                  = "1"
	from_sub_port              = "2"
	to_card                    = "1"
	to_port                    = "1"
	to_sub_port                = "2"
}

resource "aci_access_port_selector" "leaf201_Eth1-01-3" {
	leaf_interface_profile_dn  = aci_leaf_interface_profile.leaf201.id
	description                = "None"
	name                       = "Eth1-01-3"
	access_port_selector_type  = "range"
}

resource "aci_access_sub_port_block" "leaf201_Eth1-01-3" {
	depends_on                 = [aci_leaf_interface_profile.leaf201]
	access_port_selector_dn    = aci_access_port_selector.leaf201_Eth1-01-3.id
	name                       = "block3"
	from_card                  = "1"
	from_port                  = "1"
	from_sub_port              = "3"
	to_card                    = "1"
	to_port                    = "1"
	to_sub_port                = "3"
}

resource "aci_access_port_selector" "leaf201_Eth1-01-4" {
	leaf_interface_profile_dn  = aci_leaf_interface_profile.leaf201.id
	description                = "None"
	name                       = "Eth1-01-4"
	access_port_selector_type  = "range"
}

resource "aci_access_sub_port_block" "leaf201_Eth1-01-4" {
	depends_on                 = [aci_leaf_interface_profile.leaf201]
	access_port_selector_dn    = aci_access_port_selector.leaf201_Eth1-01-4.id
	name                       = "block4"
	from_card                  = "1"
	from_port                  = "1"
	from_sub_port              = "4"
	to_card                    = "1"
	to_port                    = "1"
	to_sub_port                = "4"
}

resource "aci_leaf_access_bundle_policy_group" "r143b_fp01_vpc" {
	description 				       = "r143b-fp01-vpc"
	name 						       = "r143b_fp01_vpc"
	lag_t 						       = "link"
	relation_infra_rs_att_ent_p	       = "uni/infra/attentp-access_aep"
	relation_infra_rs_cdp_if_pol       = "uni/infra/cdpIfP-cdp_Enabled"
	relation_infra_rs_h_if_pol	       = "uni/infra/hintfpol-inherit_Auto"
	relation_infra_rs_lacp_pol         = "uni/infra/lldpIfP-lacp_Active"
	relation_infra_rs_lldp_if_pol      = "uni/infra/lldpIfP-lldp_Enabled"
	relation_infra_rs_mcp_if_pol       = "uni/infra/mcpIfP-mcp_Enabled"
	relation_infra_rs_mon_if_infra_pol = "uni/infra/moninfra-default"
	relation_infra_rs_stp_if_pol       = "uni/infra/ifPol-BPDU_fg"
}

resource "aci_rest" "leaf201_Eth1-1-01_pg" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf201/hports-Eth1-1-01-typ-range/rsaccBaseGrp.json"
	class_name	= "infraRsAccBaseGrp"
	payload		= <<EOF
{
    "infraRsAccBaseGrp": {
        "attributes": {
            "tDn": "uni/infra/funcprof/accbundle-r143b_fp01_vpc"
        },
        "children": []
    }
}
	EOF
}

resource "aci_access_sub_port_block" "leaf201_Eth1-1-01_descr" {
	depends_on                 = [aci_access_sub_port_block.leaf201_Eth1-1-01]
	access_port_selector_dn    = aci_access_port_selector.leaf201_Eth1-1-01.id
	description                = "r143b-fp01-Eth1/1"
}

resource "aci_leaf_access_bundle_policy_group" "r143c_fp02_vpc" {
	description 				       = "r143c-fp02-vpc"
	name 						       = "r143c_fp02_vpc"
	lag_t 						       = "link"
	relation_infra_rs_att_ent_p	       = "uni/infra/attentp-access_aep"
	relation_infra_rs_cdp_if_pol       = "uni/infra/cdpIfP-cdp_Enabled"
	relation_infra_rs_h_if_pol	       = "uni/infra/hintfpol-inherit_Auto"
	relation_infra_rs_lacp_pol         = "uni/infra/lldpIfP-lacp_Active"
	relation_infra_rs_lldp_if_pol      = "uni/infra/lldpIfP-lldp_Enabled"
	relation_infra_rs_mcp_if_pol       = "uni/infra/mcpIfP-mcp_Enabled"
	relation_infra_rs_mon_if_infra_pol = "uni/infra/moninfra-default"
	relation_infra_rs_stp_if_pol       = "uni/infra/ifPol-BPDU_fg"
}

resource "aci_rest" "leaf201_Eth1-1-02_pg" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf201/hports-Eth1-1-02-typ-range/rsaccBaseGrp.json"
	class_name	= "infraRsAccBaseGrp"
	payload		= <<EOF
{
    "infraRsAccBaseGrp": {
        "attributes": {
            "tDn": "uni/infra/funcprof/accbundle-r143c_fp02_vpc"
        },
        "children": []
    }
}
	EOF
}

resource "aci_access_sub_port_block" "leaf201_Eth1-1-02_descr" {
	depends_on                 = [aci_access_sub_port_block.leaf201_Eth1-1-02]
	access_port_selector_dn    = aci_access_port_selector.leaf201_Eth1-1-02.id
	description                = "r143c-fp02-Eth1/1"
}

resource "aci_rest" "leaf201_Eth1-1-03_pg" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf201/hports-Eth1-1-03-typ-range/rsaccBaseGrp.json"
	class_name	= "infraRsAccBaseGrp"
	payload		= <<EOF
{
    "infraRsAccBaseGrp": {
        "attributes": {
            "tDn": "uni/infra/funcprof/accportgrp-access_host_apg"
        },
        "children": []
    }
}
	EOF
}

resource "aci_access_sub_port_block" "leaf201_Eth1-1-03_descr" {
	depends_on                 = [aci_access_sub_port_block.leaf201_Eth1-1-03]
	access_port_selector_dn    = aci_access_port_selector.leaf201_Eth1-1-03.id
	description                = "143c-lab-gw1-Te0/0/4"
}

resource "aci_rest" "leaf201_Eth1-1-04_pg" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf201/hports-Eth1-1-04-typ-range/rsaccBaseGrp.json"
	class_name	= "infraRsAccBaseGrp"
	payload		= <<EOF
{
    "infraRsAccBaseGrp": {
        "attributes": {
            "tDn": "uni/infra/funcprof/accportgrp-access_host_apg"
        },
        "children": []
    }
}
	EOF
}

resource "aci_access_sub_port_block" "leaf201_Eth1-1-04_descr" {
	depends_on                 = [aci_access_sub_port_block.leaf201_Eth1-1-04]
	access_port_selector_dn    = aci_access_port_selector.leaf201_Eth1-1-04.id
	description                = "None"
}

resource "aci_leaf_access_bundle_policy_group" "r143c-netapp01-ct0_vpc" {
	description 				       = "r143c-netapp01-ct0-vpc"
	name 						       = "r143c-netapp01-ct0_vpc"
	lag_t 						       = "link"
	relation_infra_rs_att_ent_p	       = "uni/infra/attentp-access_aep"
	relation_infra_rs_cdp_if_pol       = "uni/infra/cdpIfP-cdp_Enabled"
	relation_infra_rs_h_if_pol	       = "uni/infra/hintfpol-inherit_Auto"
	relation_infra_rs_lacp_pol         = "uni/infra/lldpIfP-lacp_Active"
	relation_infra_rs_lldp_if_pol      = "uni/infra/lldpIfP-lldp_Enabled"
	relation_infra_rs_mcp_if_pol       = "uni/infra/mcpIfP-mcp_Enabled"
	relation_infra_rs_mon_if_infra_pol = "uni/infra/moninfra-default"
	relation_infra_rs_stp_if_pol       = "uni/infra/ifPol-"
}

resource "aci_rest" "leaf201_Eth1-02_pg" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf201/hports-Eth1-02-typ-range/rsaccBaseGrp.json"
	class_name	= "infraRsAccBaseGrp"
	payload		= <<EOF
{
    "infraRsAccBaseGrp": {
        "attributes": {
            "tDn": "uni/infra/funcprof/accbundle-r143c-netapp01-ct0_vpc"
        },
        "children": []
    }
}
	EOF
}

resource "aci_access_port_block" "leaf201_Eth1-02_descr" {
	access_port_selector_dn    = "uni/infra/accportprof-leaf201/hports-Eth1-02-typ-range"
	description                = "None"
}

resource "aci_leaf_access_bundle_policy_group" "r143c-netapp01-ct1_vpc" {
	description 				       = "r143c-netapp01-ct1-vpc"
	name 						       = "r143c-netapp01-ct1_vpc"
	lag_t 						       = "link"
	relation_infra_rs_att_ent_p	       = "uni/infra/attentp-access_aep"
	relation_infra_rs_cdp_if_pol       = "uni/infra/cdpIfP-cdp_Enabled"
	relation_infra_rs_h_if_pol	       = "uni/infra/hintfpol-inherit_Auto"
	relation_infra_rs_lacp_pol         = "uni/infra/lldpIfP-lacp_Active"
	relation_infra_rs_lldp_if_pol      = "uni/infra/lldpIfP-lldp_Enabled"
	relation_infra_rs_mcp_if_pol       = "uni/infra/mcpIfP-mcp_Enabled"
	relation_infra_rs_mon_if_infra_pol = "uni/infra/moninfra-default"
	relation_infra_rs_stp_if_pol       = "uni/infra/ifPol-"
}

resource "aci_rest" "leaf201_Eth1-03_pg" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf201/hports-Eth1-03-typ-range/rsaccBaseGrp.json"
	class_name	= "infraRsAccBaseGrp"
	payload		= <<EOF
{
    "infraRsAccBaseGrp": {
        "attributes": {
            "tDn": "uni/infra/funcprof/accbundle-r143c-netapp01-ct1_vpc"
        },
        "children": []
    }
}
	EOF
}

resource "aci_access_port_block" "leaf201_Eth1-03_descr" {
	access_port_selector_dn    = "uni/infra/accportprof-leaf201/hports-Eth1-03-typ-range"
	description                = "None"
}

resource "aci_rest" "leaf201_Eth1-04_pg" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf201/hports-Eth1-04-typ-range/rsaccBaseGrp.json"
	class_name	= "infraRsAccBaseGrp"
	payload		= <<EOF
{
    "infraRsAccBaseGrp": {
        "attributes": {
            "tDn": "uni/infra/funcprof/accportgrp-access_host_apg"
        },
        "children": []
    }
}
	EOF
}

resource "aci_access_port_block" "leaf201_Eth1-04_descr" {
	access_port_selector_dn    = "uni/infra/accportprof-leaf201/hports-Eth1-04-typ-range"
	description                = "None"
}

resource "aci_leaf_access_bundle_policy_group" "r143b-ucs-a_vpc" {
	description 				       = "r143b-ucs-a-vpc"
	name 						       = "r143b-ucs-a_vpc"
	lag_t 						       = "link"
	relation_infra_rs_att_ent_p	       = "uni/infra/attentp-access_aep"
	relation_infra_rs_cdp_if_pol       = "uni/infra/cdpIfP-cdp_Enabled"
	relation_infra_rs_h_if_pol	       = "uni/infra/hintfpol-inherit_Auto"
	relation_infra_rs_lacp_pol         = "uni/infra/lldpIfP-lacp_Active"
	relation_infra_rs_lldp_if_pol      = "uni/infra/lldpIfP-lldp_Enabled"
	relation_infra_rs_mcp_if_pol       = "uni/infra/mcpIfP-mcp_Enabled"
	relation_infra_rs_mon_if_infra_pol = "uni/infra/moninfra-default"
	relation_infra_rs_stp_if_pol       = "uni/infra/ifPol-"
}

resource "aci_rest" "leaf201_Eth1-05_pg" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf201/hports-Eth1-05-typ-range/rsaccBaseGrp.json"
	class_name	= "infraRsAccBaseGrp"
	payload		= <<EOF
{
    "infraRsAccBaseGrp": {
        "attributes": {
            "tDn": "uni/infra/funcprof/accbundle-r143b-ucs-a_vpc"
        },
        "children": []
    }
}
	EOF
}

resource "aci_access_port_block" "leaf201_Eth1-05_descr" {
	access_port_selector_dn    = "uni/infra/accportprof-leaf201/hports-Eth1-05-typ-range"
	description                = "None"
}

resource "aci_leaf_access_bundle_policy_group" "r143b-ucs-b_vpc" {
	description 				       = "r143b-ucs-b-vpc"
	name 						       = "r143b-ucs-b_vpc"
	lag_t 						       = "link"
	relation_infra_rs_att_ent_p	       = "uni/infra/attentp-access_aep"
	relation_infra_rs_cdp_if_pol       = "uni/infra/cdpIfP-cdp_Enabled"
	relation_infra_rs_h_if_pol	       = "uni/infra/hintfpol-inherit_Auto"
	relation_infra_rs_lacp_pol         = "uni/infra/lldpIfP-lacp_Active"
	relation_infra_rs_lldp_if_pol      = "uni/infra/lldpIfP-lldp_Enabled"
	relation_infra_rs_mcp_if_pol       = "uni/infra/mcpIfP-mcp_Enabled"
	relation_infra_rs_mon_if_infra_pol = "uni/infra/moninfra-default"
	relation_infra_rs_stp_if_pol       = "uni/infra/ifPol-"
}

resource "aci_rest" "leaf201_Eth1-06_pg" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf201/hports-Eth1-06-typ-range/rsaccBaseGrp.json"
	class_name	= "infraRsAccBaseGrp"
	payload		= <<EOF
{
    "infraRsAccBaseGrp": {
        "attributes": {
            "tDn": "uni/infra/funcprof/accbundle-r143b-ucs-b_vpc"
        },
        "children": []
    }
}
	EOF
}

resource "aci_access_port_block" "leaf201_Eth1-06_descr" {
	access_port_selector_dn    = "uni/infra/accportprof-leaf201/hports-Eth1-06-typ-range"
	description                = "None"
}

resource "aci_leaf_access_bundle_policy_group" "142b-oob_vpc" {
	description 				       = "142b-oob-vpc"
	name 						       = "142b-oob_vpc"
	lag_t 						       = "link"
	relation_infra_rs_att_ent_p	       = "uni/infra/attentp-access_aep"
	relation_infra_rs_cdp_if_pol       = "uni/infra/cdpIfP-cdp_Enabled"
	relation_infra_rs_h_if_pol	       = "uni/infra/hintfpol-inherit_Auto"
	relation_infra_rs_lacp_pol         = "uni/infra/lldpIfP-lacp_Active"
	relation_infra_rs_lldp_if_pol      = "uni/infra/lldpIfP-lldp_Enabled"
	relation_infra_rs_mcp_if_pol       = "uni/infra/mcpIfP-mcp_Enabled"
	relation_infra_rs_mon_if_infra_pol = "uni/infra/moninfra-default"
	relation_infra_rs_stp_if_pol       = "uni/infra/ifPol-"
}

resource "aci_rest" "leaf201_Eth1-07_pg" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf201/hports-Eth1-07-typ-range/rsaccBaseGrp.json"
	class_name	= "infraRsAccBaseGrp"
	payload		= <<EOF
{
    "infraRsAccBaseGrp": {
        "attributes": {
            "tDn": "uni/infra/funcprof/accbundle-142b-oob_vpc"
        },
        "children": []
    }
}
	EOF
}

resource "aci_access_port_block" "leaf201_Eth1-07_descr" {
	access_port_selector_dn    = "uni/infra/accportprof-leaf201/hports-Eth1-07-typ-range"
	description                = "None"
}

resource "aci_leaf_access_bundle_policy_group" "asgard-leaf_vpc" {
	description 				       = "asgard-leaf-vpc"
	name 						       = "asgard-leaf_vpc"
	lag_t 						       = "link"
	relation_infra_rs_att_ent_p	       = "uni/infra/attentp-access_aep"
	relation_infra_rs_cdp_if_pol       = "uni/infra/cdpIfP-cdp_Enabled"
	relation_infra_rs_h_if_pol	       = "uni/infra/hintfpol-inherit_Auto"
	relation_infra_rs_lacp_pol         = "uni/infra/lldpIfP-lacp_Active"
	relation_infra_rs_lldp_if_pol      = "uni/infra/lldpIfP-lldp_Enabled"
	relation_infra_rs_mcp_if_pol       = "uni/infra/mcpIfP-mcp_Enabled"
	relation_infra_rs_mon_if_infra_pol = "uni/infra/moninfra-default"
	relation_infra_rs_stp_if_pol       = "uni/infra/ifPol-"
}

resource "aci_rest" "leaf201_Eth1-08_pg" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf201/hports-Eth1-08-typ-range/rsaccBaseGrp.json"
	class_name	= "infraRsAccBaseGrp"
	payload		= <<EOF
{
    "infraRsAccBaseGrp": {
        "attributes": {
            "tDn": "uni/infra/funcprof/accbundle-asgard-leaf_vpc"
        },
        "children": []
    }
}
	EOF
}

resource "aci_access_port_block" "leaf201_Eth1-08_descr" {
	access_port_selector_dn    = "uni/infra/accportprof-leaf201/hports-Eth1-08-typ-range"
	description                = "asgard-leaf101-Eth1/49"
}

resource "aci_rest" "leaf201_Eth1-09_pg" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf201/hports-Eth1-09-typ-range/rsaccBaseGrp.json"
	class_name	= "infraRsAccBaseGrp"
	payload		= <<EOF
{
    "infraRsAccBaseGrp": {
        "attributes": {
            "tDn": "uni/infra/funcprof/accbundle-asgard-leaf_vpc"
        },
        "children": []
    }
}
	EOF
}

resource "aci_access_port_block" "leaf201_Eth1-09_descr" {
	access_port_selector_dn    = "uni/infra/accportprof-leaf201/hports-Eth1-09-typ-range"
	description                = "asgard-leaf102-Eth1/49"
}

resource "aci_leaf_access_bundle_policy_group" "wakanda-leaf_vpc" {
	description 				       = "wakanda-leaf-vpc"
	name 						       = "wakanda-leaf_vpc"
	lag_t 						       = "link"
	relation_infra_rs_att_ent_p	       = "uni/infra/attentp-access_aep"
	relation_infra_rs_cdp_if_pol       = "uni/infra/cdpIfP-cdp_Enabled"
	relation_infra_rs_h_if_pol	       = "uni/infra/hintfpol-inherit_Auto"
	relation_infra_rs_lacp_pol         = "uni/infra/lldpIfP-lacp_Active"
	relation_infra_rs_lldp_if_pol      = "uni/infra/lldpIfP-lldp_Enabled"
	relation_infra_rs_mcp_if_pol       = "uni/infra/mcpIfP-mcp_Enabled"
	relation_infra_rs_mon_if_infra_pol = "uni/infra/moninfra-default"
	relation_infra_rs_stp_if_pol       = "uni/infra/ifPol-"
}

resource "aci_rest" "leaf201_Eth1-10_pg" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf201/hports-Eth1-10-typ-range/rsaccBaseGrp.json"
	class_name	= "infraRsAccBaseGrp"
	payload		= <<EOF
{
    "infraRsAccBaseGrp": {
        "attributes": {
            "tDn": "uni/infra/funcprof/accbundle-wakanda-leaf_vpc"
        },
        "children": []
    }
}
	EOF
}

resource "aci_access_port_block" "leaf201_Eth1-10_descr" {
	access_port_selector_dn    = "uni/infra/accportprof-leaf201/hports-Eth1-10-typ-range"
	description                = "None"
}

resource "aci_rest" "leaf201_Eth1-11_pg" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf201/hports-Eth1-11-typ-range/rsaccBaseGrp.json"
	class_name	= "infraRsAccBaseGrp"
	payload		= <<EOF
{
    "infraRsAccBaseGrp": {
        "attributes": {
            "tDn": "uni/infra/funcprof/accbundle-wakanda-leaf_vpc"
        },
        "children": []
    }
}
	EOF
}

resource "aci_access_port_block" "leaf201_Eth1-11_descr" {
	access_port_selector_dn    = "uni/infra/accportprof-leaf201/hports-Eth1-11-typ-range"
	description                = "None"
}

resource "aci_leaf_access_bundle_policy_group" "143-oob_vpc" {
	description 				       = "143-oob-vpc"
	name 						       = "143-oob_vpc"
	lag_t 						       = "link"
	relation_infra_rs_att_ent_p	       = "uni/infra/attentp-access_aep"
	relation_infra_rs_cdp_if_pol       = "uni/infra/cdpIfP-cdp_Enabled"
	relation_infra_rs_h_if_pol	       = "uni/infra/hintfpol-inherit_Auto"
	relation_infra_rs_lacp_pol         = "uni/infra/lldpIfP-lacp_Active"
	relation_infra_rs_lldp_if_pol      = "uni/infra/lldpIfP-lldp_Enabled"
	relation_infra_rs_mcp_if_pol       = "uni/infra/mcpIfP-mcp_Enabled"
	relation_infra_rs_mon_if_infra_pol = "uni/infra/moninfra-default"
	relation_infra_rs_stp_if_pol       = "uni/infra/ifPol-"
}

resource "aci_rest" "leaf201_Eth1-12_pg" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf201/hports-Eth1-12-typ-range/rsaccBaseGrp.json"
	class_name	= "infraRsAccBaseGrp"
	payload		= <<EOF
{
    "infraRsAccBaseGrp": {
        "attributes": {
            "tDn": "uni/infra/funcprof/accbundle-143-oob_vpc"
        },
        "children": []
    }
}
	EOF
}

resource "aci_access_port_block" "leaf201_Eth1-12_descr" {
	access_port_selector_dn    = "uni/infra/accportprof-leaf201/hports-Eth1-12-typ-range"
	description                = "None"
}

resource "aci_rest" "leaf201_Eth1-13_pg" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf201/hports-Eth1-13-typ-range/rsaccBaseGrp.json"
	class_name	= "infraRsAccBaseGrp"
	payload		= <<EOF
{
    "infraRsAccBaseGrp": {
        "attributes": {
            "tDn": "uni/infra/funcprof/accbundle-143-oob_vpc"
        },
        "children": []
    }
}
	EOF
}

resource "aci_access_port_block" "leaf201_Eth1-13_descr" {
	access_port_selector_dn    = "uni/infra/accportprof-leaf201/hports-Eth1-13-typ-range"
	description                = "None"
}

resource "aci_leaf_access_bundle_policy_group" "143-dist_vpc" {
	description 				       = "143-dist-vpc"
	name 						       = "143-dist_vpc"
	lag_t 						       = "link"
	relation_infra_rs_att_ent_p	       = "uni/infra/attentp-access_aep"
	relation_infra_rs_cdp_if_pol       = "uni/infra/cdpIfP-cdp_Enabled"
	relation_infra_rs_h_if_pol	       = "uni/infra/hintfpol-inherit_Auto"
	relation_infra_rs_lacp_pol         = "uni/infra/lldpIfP-lacp_Active"
	relation_infra_rs_lldp_if_pol      = "uni/infra/lldpIfP-lldp_Enabled"
	relation_infra_rs_mcp_if_pol       = "uni/infra/mcpIfP-mcp_Enabled"
	relation_infra_rs_mon_if_infra_pol = "uni/infra/moninfra-default"
	relation_infra_rs_stp_if_pol       = "uni/infra/ifPol-"
}

resource "aci_rest" "leaf201_Eth1-14_pg" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf201/hports-Eth1-14-typ-range/rsaccBaseGrp.json"
	class_name	= "infraRsAccBaseGrp"
	payload		= <<EOF
{
    "infraRsAccBaseGrp": {
        "attributes": {
            "tDn": "uni/infra/funcprof/accbundle-143-dist_vpc"
        },
        "children": []
    }
}
	EOF
}

resource "aci_access_port_block" "leaf201_Eth1-14_descr" {
	access_port_selector_dn    = "uni/infra/accportprof-leaf201/hports-Eth1-14-typ-range"
	description                = "None"
}

resource "aci_rest" "leaf201_Eth1-15_pg" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf201/hports-Eth1-15-typ-range/rsaccBaseGrp.json"
	class_name	= "infraRsAccBaseGrp"
	payload		= <<EOF
{
    "infraRsAccBaseGrp": {
        "attributes": {
            "tDn": "uni/infra/funcprof/accbundle-143-dist_vpc"
        },
        "children": []
    }
}
	EOF
}

resource "aci_access_port_block" "leaf201_Eth1-15_descr" {
	access_port_selector_dn    = "uni/infra/accportprof-leaf201/hports-Eth1-15-typ-range"
	description                = "None"
}

