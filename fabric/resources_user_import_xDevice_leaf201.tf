# Use this Resource File to Register leaf201 with node id 201 to the Fabric
# Requirements are:
# serial: Actual Serial Number of the switch.
# name: Hostname you want to assign.
# node_id: unique ID used to identify the switch in the APIC.
#   in the "Cisco ACI Object Naming and Numbering: Best Practice
#   The recommendation is that the Spines should be 101-199
#   and leafs should start at 200+ thru 4000.  As the number of
#   spines should always be less than the number of leafs
#   https://www.cisco.com/c/en/us/td/docs/switches/datacenter/aci/apic/sw/kb/b-Cisco-ACI-Naming-and-Numbering.html#id_107280
# node_type: uremote-leaf-wan or unspecified.
# role: spine, leaf.
# pod_id: Typically this will be one unless you are running multipod.

resource "aci_fabric_node_member" "leaf201" {
	serial    = "TEP-1-101"
	name      = "leaf201"
	node_id   = "201"
	node_type = "unspecified"
	role      = "leaf"
	pod_id    = "1"
}

resource "aci_rest" "oob_mgmt_leaf201" {
	path		= "/api/node/mo/uni/tn-mgmt.json"
	class_name	= "mgmtRsOoBStNode"
	payload		= <<EOF
{
    "mgmtRsOoBStNode": {
        "attributes": {
            "dn": "uni/tn-mgmt/mgmtp-default/oob-default/rsooBStNode-[topology/pod-1/node-201]",
            "addr": "198.18.1.201/24",
            "gw": "198.18.1.1",
            "tDn": "topology/pod-1/node-201",
            "v6Addr": "::",
            "v6Gw": "::"
        }
    }
}
	EOF
}

resource "aci_rest" "inb_mgmt_leaf201" {
	depends_on		= [aci_rest.inb_mgmt_default_epg]
	path		= "/api/node/mo/uni/tn-mgmt.json"
	class_name	= "mgmtRsInBStNode"
	payload		= <<EOF
{
    "mgmtRsInBStNode": {
        "attributes": {
            "dn": "uni/tn-mgmt/mgmtp-default/inb-default/rsinBStNode-[topology/pod-1/node-201]",
            "addr": "198.18.2.201/24",
            "gw": "198.18.2.1",
            "tDn": "topology/pod-1/node-201",
            "v6Addr": "::",
            "v6Gw": "::"
        }
    }
}
	EOF
}

resource "aci_rest" "maint_grp_leaf201" {
	path		= "/api/node/mo/uni/fabric/maintgrp-switch_MgA.json"
	class_name	= "maintMaintGrp"
	payload		= <<EOF
{
    "maintMaintGrp": {
        "attributes": {
            "dn": "uni/fabric/maintgrp-switch_MgA"
        },
        "children": [
            {
                "fabricNodeBlk": {
                    "attributes": {
                        "dn": "uni/fabric/maintgrp-switch_MgA/nodeblk-blk201-201",
                        "name": "blk201-201",
                        "from_": "201",
                        "to_": "201",
                        "rn": "nodeblk-blk201-201"
                    }
                }
            }
        ]
    }
}
	EOF
}

resource "aci_leaf_interface_profile" "leaf201" {
	name   = "leaf201"
}

resource "aci_leaf_profile" "leaf201" {
	name                           = "leaf201"
	relation_infra_rs_acc_port_p   = [aci_leaf_interface_profile.leaf201.id]
	leaf_selector {
		name                    = "leaf201"
		switch_association_type = "range"
		node_block {
			name  = "leaf201"
			from_ = "201"
			to_   = "201"
		}
	}
}

resource "aci_rest" "leaf_policy_group_leaf201" {
	depends_on		= [aci_leaf_profile.leaf201]
	path		= "/api/node/mo/uni/infra/nprof-leaf201/leaves-leaf201-typ-range.json"
	class_name	= "infraLeafS"
	payload		= <<EOF
{
    "infraLeafS": {
        "attributes": {
            "dn": "uni/infra/nprof-leaf201/leaves-leaf201-typ-range"
        },
        "children": [
            {
                "infraRsAccNodePGrp": {
                    "attributes": {
                        "tDn": "uni/infra/funcprof/accnodepgrp-default"
                    },
                    "children": []
                }
            }
        ]
    }
}
	EOF
}

resource "aci_access_port_selector" "leaf201_1" {
	for_each                   = var.port-blocks-54
	leaf_interface_profile_dn  = aci_leaf_interface_profile.leaf201.id
	name                       = "Eth1${each.value.name}"
	access_port_selector_type  = "range"
}

resource "aci_access_port_block" "leaf201_1" {
	depends_on                   = [aci_leaf_interface_profile.leaf201]
	for_each                   = var.port-blocks-54
	access_port_selector_dn    = aci_access_port_selector.leaf201_1[each.key].id
	name                       = "Eth1${each.value.name}"
	from_card                  = "1"
	from_port                  = each.value.port
	to_card                    = "1"
	to_port                    = each.value.port
}
