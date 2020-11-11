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
	for_each    = var.interface_policies
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

resource "aci_l3_domain_profile" "default" {
	for_each    = var.l3dom_profile
	name        = each.value.name
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

resource "aci_physical_domain" "default" {
	for_each    = var.physical_domain
	name        = each.value.name
}

resource "aci_vlan_pool" "default" {
	for_each    = var.vlan_pool
	name        = each.value.name
	alloc_mode  = each.value.alloc_mode
}

resource "aci_ranges" "default" {
  vlan_pool_dn	= "uni/infra/vlanns-[msite_vl-pool]-static"
  _from		= "vlan-4"
  to		= "vlan-4"
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

resource "aci_rest" "phys_to_vl-pool" {
	for_each   = var.physical_domain
	path       = "/api/node/mo/uni/phys-[${each.value.name}].json"
	class_name = "physDomP"
	payload    = <<EOF
{
    "physDomP": {
        "attributes": {
            "dn": "uni/phys-${each.value.name}",
            "name": "${each.value.name}",
        },
        "children": [
            {
                "infraRsVlanNs": {
                    "attributes": {
                        "rn": "rsvlanNs",
                        "tDn": "uni/infra/vlanns-[${each.value.vl-pool}]-static"
                    }
                }
            }
        ]
    }
}
	EOF
}

resource "aci_rest" "l3_to_vl-pool" {
	for_each   = var.l3dom_profile
	path       = "/api/node/mo/uni/l3dom-[${each.value.name}].json"
	class_name = "physDomP"
	payload    = <<EOF
{
    "l3extDomP": {
        "attributes": {
            "dn": "uni/l3dom-${each.value.name}",
            "name": "${each.value.name}",
        },
        "children": [
            {
                "infraRsVlanNs": {
                    "attributes": {
                        "rn": "rsvlanNs",
                        "tDn": "uni/infra/vlanns-[${each.value.vl-pool}]-static"
                    }
                }
            }
        ]
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

