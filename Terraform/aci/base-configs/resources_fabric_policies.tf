resource "aci_attachable_access_entity_profile" "default" {
	for_each    = var.aep_policies
	description = each.value.description
	name        = each.value.name
}

resource "aci_cdp_interface_policy" "default" {
	for_each    = var.cdp_policies
	name        = each.value.name
	admin_st    = each.value.admin_st
}

resource "aci_fabric_if_pol" "default" {
	for_each    = var.Link_Level_policies
	name        = each.value.name
	description = each.value.description
	auto_neg    = each.value.auto_neg
	speed       = each.value.speed
}

resource "aci_firmware_group" "default" {
	for_each   			= var.fwg_policies
	name       			= each.value.name
	firmware_group_type = each.value.firmware_group_type
}

resource "aci_interface_fc_policy" "default" {
	for_each    = var.int_fc_policies
	name        = each.value.name
	port_mode	= each.value.port_mode
	speed		= each.value.speed
	trunk_mode  = each.value.trunk_mode
}

resource "aci_lacp_policy" "default" {
	for_each    = var.lacp_policies
	description = each.value.description
	name        = each.value.name
	mode        = each.value.mode
}

resource "aci_lldp_interface_policy" "default" {
	for_each    = var.lldp_policies
	description = each.value.description
	name        = each.value.name
	admin_rx_st = each.value.admin_rx_st
	admin_tx_st = each.value.admin_tx_st
}

resource "aci_miscabling_protocol_interface_policy" "default" {
	for_each    = var.mcp_policies
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
	for_each    			  = var.l3dom_profile
	name        			  = each.value.name
	relation_infra_rs_vlan_ns = "uni/infra/vlanns-[${each.value.vl_pool}]-static"
}

resource "aci_physical_domain" "default" {
	for_each    = var.physical_domain
	name        = each.value.name
	relation_infra_rs_vlan_ns = "uni/infra/vlanns-[${each.value.vl_pool}]-static"
}

resource "aci_ranges" "default" {
  vlan_pool_dn	= "uni/infra/vlanns-[msite_vl-pool]-static"
  _from		= "vlan-4"
  to		= "vlan-4"
}

resource "aci_rest" "stp-policies" {
	for_each   = var.stp_policies
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

resource "aci_rest" "default-oob" {
	path       = "/api/node/mo/uni/fabric/connectivityPrefs.json"
	class_name = "mgmtConnectivityPrefs"
	payload    = <<EOF
{
	"mgmtConnectivityPrefs": {
		"attributes": {
			"dn": "uni/fabric/connectivityPrefs",
			"interfacePref": "ooband"
		},
		"children": []
	}
}
	EOF
}


resource "aci_rest" "fabric_best_practice" {
	path       = "/api/node/mo/uni/fabric.json"
	class_name = "fabricInst"
	payload    = <<EOF
{
    "fabricInst": {
        "attributes": {
            "dn": "uni/fabric"
        },
        "children": [
            {
                "isisDomPol": {
                    "attributes": {
                        "dn": "uni/fabric/isisDomP-default",
                        "rn": "isisDomP-default",
                        "redistribMetric": "63"
					},
					"children": []
				}
			},
			{
				"coopPol": {
					"attributes": {
						"dn": "uni/fabric/pol-default",
						"rn": "pol-default",
						"type": "strict"
					},
					"children": []
				}
			}
		]
	}
}
	EOF
}

resource "aci_rest" "infra_best_practice" {
	path       = "/api/node/mo/uni/infra.json"
	class_name = "infraInfra"
	payload    = <<EOF
{
	"infraInfra": {
		"attributes": {
			"dn": "uni/infra",
		},
		"children": [
			{
				"infraSetPol": {
					"attributes": {
						"dn": "uni/infra/settings",
						"domainValidation": "true",
						"enforceSubnetCheck": "true"
					},
					"children": []
				}
			},
			{
				"epIpAgingP": {
					"attributes": {
						"dn": "uni/infra/ipAgingP-default",
						"rn": "ipAgingP-default",
						"adminSt": "enabled"
					},
					"children": []
				}
			},
			{
				"epControlP": {
					"attributes": {
						"dn": "uni/infra/epCtrlP-default",
						"rn": "epCtrlP-default",
						"adminSt": "enabled"
					},
					"children": []
				}
			}
		]
	}
}
	EOF
}

resource "aci_rest" "web_interface_timeout" {
	path       = "/api/node/mo/uni/userext/pkiext/webtokendata.json"
	class_name = "pkiWebTokenData"
	payload    = <<EOF
{
	"pkiWebTokenData": {
		"attributes": {
			"dn": "uni/userext/pkiext/webtokendata",
			"uiIdleTimeoutSeconds": "65525"
		},
		"children": []
	}
}
	EOF
}

resource "aci_contract" "mgmt_ctx" {
	tenant_dn   = aci_tenant.mgmt.id
	description = "Default Mgmt Contract"
	name        = "mgmt_ctx"
	scope       = "tenant"
	filter {
		  description = "Mgmt Traffic"
		  filter_entry {
				entry_description	= "Allow https"
			filter_entry_name   	= "https"
				d_from_port        	= "https"
				d_to_port	        = "https"
				ether_t             = "ipv4"
				prot            	= "tcp"
				stateful			= "yes"  
		  }
		  filter_entry {
				entry_description   = "Allow icmp"
			filter_entry_name   	= "icmp"
				d_from_port        	= "unspecified"
				d_to_port        	= "unspecified"
				ether_t             = "ipv4"
				prot           		= "icmp"
		  }
		  filter_entry {
				entry_description   = "Allow SNMP"
			filter_entry_name   	= "snmp"
				d_from_port        	= "161"
				d_to_port        	= "162"
				ether_t             = "ipv4"
				prot           		= "udp"
		  }
		  filter_entry {
				entry_description   = "Allow ssh"
			filter_entry_name   	= "ssh"
				d_from_port        	= "22"
				d_to_port        	= "22"
				ether_t             = "ipv4"
				prot           		= "tcp" 
				stateful			= "yes" 
		  }
		  filter_name  = "Remote_Mgmt"
	}
}

resource "aci_contract_subject" "Mgmt_Subj" {
	contract_dn					 = aci_contract.mgmt_ctx.id
	name						 = "Mgmt_Subj"
	relation_vz_rs_subj_filt_att = ["uni/tn-mgmt/flt-Remote_Mgmt"]
	rev_flt_ports				 = "yes"
}

resource "aci_epg_to_contract" "inb-inb_epg" {
    application_epg_dn = aci_application_epg.inb_epg.id
    contract_dn  = aci_contract.mgmt_ctx.id
    contract_type = "provider"
}

resource "aci_rest" "oob_mgmt_ctx" {
	path       = "/api/node/mo/uni/tn-mgmt/oobbrc-oob_mgmt_ctx.json"
	class_name = "vzOOBBrCP"
	payload    = <<EOF
{
	"vzOOBBrCP": {
		"attributes": {
			"dn": "uni/tn-mgmt/oobbrc-oob_mgmt_ctx",
			"name": "oob_mgmt_ctx",
			"scope": "tenant",
			"rn": "oobbrc-oob_mgmt_ctx",
			"status": "created"
		},
		"children": [
			{
				"vzSubj": {
					"attributes": {
						"dn": "uni/tn-mgmt/oobbrc-oob_mgmt_ctx/subj-oob_mgmt_Subj",
						"name": "oob_mgmt_Subj",
						"rn": "subj-oob_mgmt_Subj",
						"status": "created"
					},
					"children": [
						{
							"vzRsSubjFiltAtt": {
								"attributes": {
									"status": "created,modified",
									"tnVzFilterName": "Remote_Mgmt"
								},
								"children": []
							}
						}
					]
				}
			}
		]
	}
}
	EOF
}

resource "aci_rest" "snmp_cg" {
	for_each   = var.snmp_policies
	path       = "/api/node/mo/uni/fabric/snmppol-default/clgrp-${each.value.name}_Clients.json"
	class_name = "snmpClientGrpP"
	payload    = <<EOF
{
	"snmpClientGrpP": {
		"attributes": {
			"dn": "uni/fabric/snmppol-default/clgrp-${each.value.name}_Clients",
			"name": "${each.value.name}_Clients",
			"descr": "SNMP Clients allowed on ${each.value.name} Mgmt",
			"rn": "clgrp-${each.value.name}_Clients",
			"status": "created"
		},
		"children": [
			{
				"snmpRsEpg": {
					"attributes": {
						"tDn": "uni/tn-mgmt/mgmtp-default/${each.value.epg}",
						"status": "created"
					},
					"children": []
				}
			}
		]
	}
}
	EOF
}