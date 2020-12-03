# Use this Resource File to Register leaf202 with node id 202 to the Fabric
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

resource "aci_fabric_node_member" "leaf202" {
	serial    = "TEP-1-102"
	name      = "leaf202"
	node_id   = "202"
	node_type = "unspecified"
	role      = "leaf"
	pod_id    = "1"
}

resource "aci_rest" "oob_mgmt_leaf202" {
	path		= "/api/node/mo/uni/tn-mgmt.json"
	class_name	= "mgmtRsOoBStNode"
	payload		= <<EOF
{
    "mgmtRsOoBStNode": {
        "attributes": {
            "dn": "uni/tn-mgmt/mgmtp-default/oob-default/rsooBStNode-[topology/pod-1/node-202]",
            "addr": "198.18.1.202/24",
            "gw": "198.18.1.1",
            "tDn": "topology/pod-1/node-202",
            "v6Addr": "::",
            "v6Gw": "::"
        }
    }
}
	EOF
}

resource "aci_rest" "inb_mgmt_leaf202" {
	path		= "/api/node/mo/uni/tn-mgmt.json"
	class_name	= "mgmtRsInBStNode"
	payload		= <<EOF
{
    "mgmtRsInBStNode": {
        "attributes": {
            "dn": "uni/tn-mgmt/mgmtp-default/inb-default/rsinBStNode-[topology/pod-1/node-202]",
            "addr": "198.18.2.202/24",
            "gw": "198.18.2.1",
            "tDn": "topology/pod-1/node-202",
            "v6Addr": "::",
            "v6Gw": "::"
        }
    }
}
	EOF
}

resource "aci_rest" "maint_grp_leaf202" {
	path		= "/api/node/mo/uni/fabric/maintgrp-switch_MgB.json"
	class_name	= "maintMaintGrp"
	payload		= <<EOF
{
    "maintMaintGrp": {
        "attributes": {
            "dn": "uni/fabric/maintgrp-switch_MgB"
        },
        "children": [
            {
                "fabricNodeBlk": {
                    "attributes": {
                        "dn": "uni/fabric/maintgrp-switch_MgB/nodeblk-blk202-202",
                        "name": "blk202-202",
                        "from_": "202",
                        "to_": "202",
                        "rn": "nodeblk-blk202-202"
                    }
                }
            }
        ]
    }
}
	EOF
}

resource "aci_leaf_interface_profile" "leaf202" {
	name   = "leaf202"
}

resource "aci_leaf_profile" "leaf202" {
	name                           = "leaf202"
	relation_infra_rs_acc_port_p   = [aci_leaf_interface_profile.leaf202.id]
	leaf_selector {
		name                    = "leaf202"
		switch_association_type = "range"
		node_block {
			name  = "leaf202"
			from_ = "202"
			to_   = "202"
		}
	}
}

resource "aci_rest" "leaf_policy_group_leaf202" {
	path		= "/api/node/mo/uni/infra/nprof-leaf202/leaves-leaf202-typ-range.json"
	class_name	= "infraLeafS"
	payload		= <<EOF
{
    "infraLeafS": {
        "attributes": {
            "dn": "uni/infra/nprof-leaf202/leaves-leaf202-typ-range"
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

resource "aci_access_port_selector" "leaf202_1" {
	for_each                   = var.port-blocks-54
	leaf_interface_profile_dn  = aci_leaf_interface_profile.leaf202.id
	name                       = "Eth1-${each.value.name}"
	access_port_selector_type  = "range"
}

resource "aci_access_port_block" "leaf202_1" {
	for_each                   = var.port-blocks-54
	access_port_selector_dn    = aci_access_port_selector.leaf202_1[each.key].id
	description                = each.value.description
	name                       = "Eth1-${each.value.name}"
	from_card                  = "1"
	from_port                  = each.value.port
	to_card                    = "1"
	to_port                    = each.value.port
}

