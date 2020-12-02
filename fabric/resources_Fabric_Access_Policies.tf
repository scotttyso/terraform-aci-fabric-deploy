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

resource "aci_leaf_access_port_policy_group" "inband_apg" {
	description 				  = "Inband port-group policy"
	name 						  = "inband_ap"
	relation_infra_rs_h_if_pol	  = "uni/infra/hintfpol-inherit_Auto"
	relation_infra_rs_mcp_if_pol  = "uni/infra/mcpIfP-mcp_Enabled"
	relation_infra_rs_lldp_if_pol = "uni/infra/lldpIfP-lldp_Enabled"
    relation_infra_rs_stp_if_pol  = "uni/infra/ifPol-BPDU_fg"
	relation_infra_rs_att_ent_p	  = "uni/infra/attentp-access_aep"
}

resource "aci_leaf_access_port_policy_group" "access_host_apg" {
	description 				  = "Template for a Host Access Port"
	name 						  = "access_host_ap"
	relation_infra_rs_h_if_pol	  = "uni/infra/hintfpol-inherit_Auto"
	relation_infra_rs_cdp_if_pol  = "uni/infra/cdpIfP-cdp_Disabled"
	relation_infra_rs_mcp_if_pol  = "uni/infra/mcpIfP-mcp_Enabled"
	relation_infra_rs_lldp_if_pol = "uni/infra/lldpIfP-lldp_Enabled"
    relation_infra_rs_stp_if_pol  = "uni/infra/ifPol-BPDU_fg"
	relation_infra_rs_att_ent_p	  = "uni/infra/attentp-access_aep"
}

resource "aci_rest" "breakout_4x10g" {
	path		= "/api/node/mo/uni/infra/funcprof/brkoutportgrp-4x10g_pg.json"
	class_name	= "infraBrkoutPortGrp"
	payload		= <<EOF
{
    "infraBrkoutPortGrp": {
        "attributes": {
            "dn": "uni/infra/funcprof/brkoutportgrp-4x10g_pg",
            "brkoutMap": "10g-4x"
            "name": "4x10g_pg"
            "descr": "Breakout of 40G to 4x10g.  Configured by Brahma startup Wizard"
            "rn": "brkoutportgrp-4x10g_pg"
        },
        "children": []
    }
}
	EOF
}

resource "aci_rest" "breakout" {
	for_each    = var.breakouts
	path		= "/api/node/mo/uni/infra/funcprof/brkoutportgrp-${each.value.name}.json"
	class_name	= "infraBrkoutPortGrp"
	payload		= <<EOF
{
    "infraBrkoutPortGrp": {
        "attributes": {
            "dn": "uni/infra/funcprof/brkoutportgrp-${each.value.name}",
            "brkoutMap": "${each.value.map}",
            "name": "${each.value.name}",
            "descr": "Breakout of ${each.value.description}.  Configured by Brahma startup Wizard",
            "rn": "brkoutportgrp-${each.value.name}"
        },
        "children": []
    }
}
	EOF
}

resource "aci_rest" "vpc_description" {
	path		= "/api/node/mo/uni/fabric/protpol.json"
	class_name	= "fabricProtPol"
	payload		= <<EOF
{
    "fabricProtPol": {
        "attributes": {
            "dn": "uni/fabric/protpol",
            "descr": "VPC Pair Configuration.  Configured by Brahma startup Wizard"
        },
        "children": []
    }
}
	EOF
}

resource "aci_rest" "Leaf_Policy_Group" {
	path		= "/api/node/mo/uni/infra/funcprof/accnodepgrp-default.json"
	class_name	= "infraAccNodePGrp"
	payload		= <<EOF
{
	"infraAccNodePGrp": {
		"attributes": {
			"dn": "uni/infra/funcprof/accnodepgrp-default",
			"name": "default",
			"descr": "Default Policy Group for Leaf Switches - Created by Brahma Startup Script.",
			"rn": "accnodepgrp-default"
		},
		"children": [
			{
				"infraRsMstInstPol": {
					"attributes": {
						"tnStpInstPolName": "default"
					},
					"children": []
				}
			},
			{
				"infraRsTopoctrlFwdScaleProfPol": {
					"attributes": {
						"tnTopoctrlFwdScaleProfilePolName": "default"
					},
					"children": []
				}
			},
			{
				"infraRsTopoctrlFastLinkFailoverInstPol": {
					"attributes": {
						"tnTopoctrlFastLinkFailoverInstPolName": "default"
					},
					"children": []
				}
			},
			{
				"infraRsL2NodeAuthPol": {
					"attributes": {
						"tnL2NodeAuthPolName": "default"
					},
					"children": []
				}
			},
			{
				"infraRsIaclLeafProfile": {
					"attributes": {
						"tnIaclLeafProfileName": "default"
					},
					"children": []
				}
			},
			{
				"infraRsEquipmentFlashConfigPol": {
					"attributes": {
						"tnEquipmentFlashConfigPolName": "default"
					},
					"children": []
				}
			},
			{
				"infraRsLeafPGrpToCdpIfPol": {
					"attributes": {
						"tnCdpIfPolName": "cdp_Enabled"
					},
					"children": []
				}
			},
			{
				"infraRsLeafPGrpToLldpIfPol": {
					"attributes": {
						"tnLldpIfPolName": "lldp_Enabled"
					},
					"children": []
				}
			},
			{
				"infraRsBfdIpv4InstPol": {
					"attributes": {
						"tnBfdIpv4InstPolName": "default"
					},
					"children": []
				}
			},
			{
				"infraRsBfdIpv6InstPol": {
					"attributes": {
						"tnBfdIpv6InstPolName": "default"
					},
					"children": []
				}
			},
			{
				"infraRsFcInstPol": {
					"attributes": {
						"tnFcInstPolName": "default"
					},
					"children": []
				}
			},
			{
				"infraRsPoeInstPol": {
					"attributes": {
						"tnPoeInstPolName": "default"
					},
					"children": []
				}
			},
			{
				"infraRsFcFabricPol": {
					"attributes": {
						"tnFcFabricPolName": "default"
					},
					"children": []
				}
			},
			{
				"infraRsMonNodeInfraPol": {
					"attributes": {
						"tnMonInfraPolName": "default"
					},
					"children": []
				}
			},
			{
				"infraRsNetflowNodePol": {
					"attributes": {
						"tnNetflowNodePolName": "default"
					},
					"children": []
				}
			},
			{
				"infraRsLeafCoppProfile": {
					"attributes": {
						"tnCoppLeafProfileName": "default"
					},
					"children": []
				}
			}
		]
	}
}
	EOF
}

resource "aci_rest" "Spine_Policy_Group" {
	path		= "/api/node/mo/uni/infra/funcprof/spaccnodepgrp-default.json"
	class_name	= "infraSpineAccNodePGrp"
	payload		= <<EOF
{
	"infraSpineAccNodePGrp": {
		"attributes": {
			"dn": "uni/infra/funcprof/spaccnodepgrp-default",
			"name": "default",
			"descr": "Default Policy Group for Spine Switches - Created by Brahma Startup Script.",
			"rn": "spaccnodepgrp-default"
		},
		"children": [
			{
				"infraRsSpineCoppProfile": {
					"attributes": {
						"tnCoppSpineProfileName": "default"
					},
					"children": []
				}
			},
			{
				"infraRsSpineBfdIpv4InstPol": {
					"attributes": {
						"tnBfdIpv4InstPolName": "default"
					},
					"children": []
				}
			},
			{
				"infraRsSpineBfdIpv6InstPol": {
					"attributes": {
						"tnBfdIpv6InstPolName": "default"
					},
					"children": []
				}
			},
			{
				"infraRsIaclSpineProfile": {
					"attributes": {
						"tnIaclSpineProfileName": "default"
					},
					"children": []
				}
			},
			{
				"infraRsSpinePGrpToCdpIfPol": {
					"attributes": {
						"tnCdpIfPolName": "cdp_Enabled"
					},
					"children": []
				}
			},
			{
				"infraRsSpinePGrpToLldpIfPol": {
					"attributes": {
						"tnLldpIfPolName": "lldp_Enabled"
					},
					"children": []
				}
			}
		]
	}
}
	EOF
}