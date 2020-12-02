# Use this Resource File to Register spine101 with node id 101 to the Fabric
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

resource "aci_fabric_node_member" "spine101" {
	serial    = "TEP-1-103"
	name      = "spine101"
	node_id   = "101"
	node_type = "unspecified"
	role      = "spine"
	pod_id    = "1"
}

resource "aci_rest" "oob_mgmt_spine101" {
	path		= "/api/node/mo/uni/tn-mgmt.json"
	class_name	= "mgmtRsOoBStNode"
	payload		= <<EOF
{
    "mgmtRsOoBStNode": {
        "attributes": {
            "dn": "uni/tn-mgmt/mgmtp-default/oob-default/rsooBStNode-[topology/pod-1/node-101]",
            "addr": "198.18.1.101/24",
            "gw": "198.18.1.1",
            "tDn": "topology/pod-1/node-101",
            "v6Addr": "::",
            "v6Gw": "::"
        }
    }
}
	EOF
}

resource "aci_rest" "inb_mgmt_spine101" {
	path		= "/api/node/mo/uni/tn-mgmt.json"
	class_name	= "mgmtRsInBStNode"
	payload		= <<EOF
{
    "mgmtRsInBStNode": {
        "attributes": {
            "dn": "uni/tn-mgmt/mgmtp-default/inb-default/rsinBStNode-[topology/pod-1/node-101]",
            "addr": "198.18.2.101/24",
            "gw": "198.18.2.1",
            "tDn": "topology/pod-1/node-101",
            "v6Addr": "::",
            "v6Gw": "::"
        }
    }
}
	EOF
}

resource "aci_rest" "maint_grp_spine101" {
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
                        "dn": "uni/fabric/maintgrp-switch_MgA/nodeblk-blk101-101",
                        "name": "blk101-101",
                        "from_": "101",
                        "to_": "101",
                        "rn": "nodeblk-blk101-101"
                    }
                }
            }
        ]
    }
}
	EOF
}

resource "aci_spine_profile" "spine101_SwSel" {
	name = "spine101_SwSel"
}

resource "aci_spine_interface_profile" "spine101_IntProf" {
	name = "spine101_IntProf"
}

resource "aci_spine_switch_association" "spine101" {
	spine_profile_dn              = aci_spine_profile.spine101_SwSel.id
	name                          = "spine101"
	spine_switch_association_type = "range"
}

resource "aci_spine_port_selector" "spine101" {
	spine_profile_dn              = aci_spine_profile.spine101_SwSel.id
	tdn                           = aci_spine_interface_profile.spine101_IntProf.id
}

resource "aci_rest" "spine_policy_group_spine101_SwSel" {
	path		= "/api/node/mo/uni/infra/spprof-spine101_SwSel/spines-spine101-typ-range.json"
	class_name	= "infraSpineS"
	payload		= <<EOF
{
    "infraSpineS": {
        "attributes": {
            "dn": "uni/infra/spprof-spine101_SwSel/spines-spine101-typ-range"
        },
        "children": [
            {
                "infraRsSpineAccNodePGrp": {
                    "attributes": {
                        "tDn": "uni/infra/funcprof/spaccnodepgrp-default"
                    },
                    "children": []
                }
            }
        ]
    }
}
	EOF
}

resource "aci_rest" "spine101_1_IntProf" {
	for_each         = var.port-selector-36
	path             = "/api/node/mo/uni/infra/spaccportprof-spine101_IntProf/shports-Eth1-${each.value.name}-typ-range.json"
	class_name       = "infraSHPortS"
	payload          = <<EOF
{
    "infraSHPortS": {
        "attributes": {
            "dn": "uni/infra/spaccportprof-spine101_IntProf/shports-Eth1-${each.value.name}-typ-range",
            "name": "Eth1-${each.value.name}",
            "rn": "shports-Eth1-${each.value.name}-typ-range"
        },
        "children": [
            {
                "infraPortBlk": {
                    "attributes": {
                        "dn": "uni/infra/spaccportprof-spine101_IntProf/shports-Eth1-${each.value.name}-typ-range/portblk-block2",
                        "fromCard": "1",
                        "fromPort": "${each.value.name}",
                        "toCard": "1",
                        "toPort": "${each.value.name}",
                        "name": "block2",
                        "rn": "portblk-block2"
                    }
                }
            }
        ]
    }
}
	EOF
}

resource "aci_rest" "spine101_2_IntProf" {
	for_each         = var.port-selector-36
	path             = "/api/node/mo/uni/infra/spaccportprof-spine101_IntProf/shports-Eth2-${each.value.name}-typ-range.json"
	class_name       = "infraSHPortS"
	payload          = <<EOF
{
    "infraSHPortS": {
        "attributes": {
            "dn": "uni/infra/spaccportprof-spine101_IntProf/shports-Eth2-${each.value.name}-typ-range",
            "name": "Eth2-${each.value.name}",
            "rn": "shports-Eth2-${each.value.name}-typ-range"
        },
        "children": [
            {
                "infraPortBlk": {
                    "attributes": {
                        "dn": "uni/infra/spaccportprof-spine101_IntProf/shports-Eth2-${each.value.name}-typ-range/portblk-block2",
                        "fromCard": "2",
                        "fromPort": "${each.value.name}",
                        "toCard": "2",
                        "toPort": "${each.value.name}",
                        "name": "block2",
                        "rn": "portblk-block2"
                    }
                }
            }
        ]
    }
}
	EOF
}

resource "aci_rest" "spine101_3_IntProf" {
	for_each         = var.port-selector-36
	path             = "/api/node/mo/uni/infra/spaccportprof-spine101_IntProf/shports-Eth3-${each.value.name}-typ-range.json"
	class_name       = "infraSHPortS"
	payload          = <<EOF
{
    "infraSHPortS": {
        "attributes": {
            "dn": "uni/infra/spaccportprof-spine101_IntProf/shports-Eth3-${each.value.name}-typ-range",
            "name": "Eth3-${each.value.name}",
            "rn": "shports-Eth3-${each.value.name}-typ-range"
        },
        "children": [
            {
                "infraPortBlk": {
                    "attributes": {
                        "dn": "uni/infra/spaccportprof-spine101_IntProf/shports-Eth3-${each.value.name}-typ-range/portblk-block2",
                        "fromCard": "3",
                        "fromPort": "${each.value.name}",
                        "toCard": "3",
                        "toPort": "${each.value.name}",
                        "name": "block2",
                        "rn": "portblk-block2"
                    }
                }
            }
        ]
    }
}
	EOF
}

resource "aci_rest" "spine101_4_IntProf" {
	for_each         = var.port-selector-36
	path             = "/api/node/mo/uni/infra/spaccportprof-spine101_IntProf/shports-Eth4-${each.value.name}-typ-range.json"
	class_name       = "infraSHPortS"
	payload          = <<EOF
{
    "infraSHPortS": {
        "attributes": {
            "dn": "uni/infra/spaccportprof-spine101_IntProf/shports-Eth4-${each.value.name}-typ-range",
            "name": "Eth4-${each.value.name}",
            "rn": "shports-Eth4-${each.value.name}-typ-range"
        },
        "children": [
            {
                "infraPortBlk": {
                    "attributes": {
                        "dn": "uni/infra/spaccportprof-spine101_IntProf/shports-Eth4-${each.value.name}-typ-range/portblk-block2",
                        "fromCard": "4",
                        "fromPort": "${each.value.name}",
                        "toCard": "4",
                        "toPort": "${each.value.name}",
                        "name": "block2",
                        "rn": "portblk-block2"
                    }
                }
            }
        ]
    }
}
	EOF
}

resource "aci_rest" "spine101_5_IntProf" {
	for_each         = var.port-selector-36
	path             = "/api/node/mo/uni/infra/spaccportprof-spine101_IntProf/shports-Eth5-${each.value.name}-typ-range.json"
	class_name       = "infraSHPortS"
	payload          = <<EOF
{
    "infraSHPortS": {
        "attributes": {
            "dn": "uni/infra/spaccportprof-spine101_IntProf/shports-Eth5-${each.value.name}-typ-range",
            "name": "Eth5-${each.value.name}",
            "rn": "shports-Eth5-${each.value.name}-typ-range"
        },
        "children": [
            {
                "infraPortBlk": {
                    "attributes": {
                        "dn": "uni/infra/spaccportprof-spine101_IntProf/shports-Eth5-${each.value.name}-typ-range/portblk-block2",
                        "fromCard": "5",
                        "fromPort": "${each.value.name}",
                        "toCard": "5",
                        "toPort": "${each.value.name}",
                        "name": "block2",
                        "rn": "portblk-block2"
                    }
                }
            }
        ]
    }
}
	EOF
}

resource "aci_rest" "spine101_6_IntProf" {
	for_each         = var.port-selector-36
	path             = "/api/node/mo/uni/infra/spaccportprof-spine101_IntProf/shports-Eth6-${each.value.name}-typ-range.json"
	class_name       = "infraSHPortS"
	payload          = <<EOF
{
    "infraSHPortS": {
        "attributes": {
            "dn": "uni/infra/spaccportprof-spine101_IntProf/shports-Eth6-${each.value.name}-typ-range",
            "name": "Eth6-${each.value.name}",
            "rn": "shports-Eth6-${each.value.name}-typ-range"
        },
        "children": [
            {
                "infraPortBlk": {
                    "attributes": {
                        "dn": "uni/infra/spaccportprof-spine101_IntProf/shports-Eth6-${each.value.name}-typ-range/portblk-block2",
                        "fromCard": "6",
                        "fromPort": "${each.value.name}",
                        "toCard": "6",
                        "toPort": "${each.value.name}",
                        "name": "block2",
                        "rn": "portblk-block2"
                    }
                }
            }
        ]
    }
}
	EOF
}

resource "aci_rest" "spine101_7_IntProf" {
	for_each         = var.port-selector-36
	path             = "/api/node/mo/uni/infra/spaccportprof-spine101_IntProf/shports-Eth7-${each.value.name}-typ-range.json"
	class_name       = "infraSHPortS"
	payload          = <<EOF
{
    "infraSHPortS": {
        "attributes": {
            "dn": "uni/infra/spaccportprof-spine101_IntProf/shports-Eth7-${each.value.name}-typ-range",
            "name": "Eth7-${each.value.name}",
            "rn": "shports-Eth7-${each.value.name}-typ-range"
        },
        "children": [
            {
                "infraPortBlk": {
                    "attributes": {
                        "dn": "uni/infra/spaccportprof-spine101_IntProf/shports-Eth7-${each.value.name}-typ-range/portblk-block2",
                        "fromCard": "7",
                        "fromPort": "${each.value.name}",
                        "toCard": "7",
                        "toPort": "${each.value.name}",
                        "name": "block2",
                        "rn": "portblk-block2"
                    }
                }
            }
        ]
    }
}
	EOF
}

resource "aci_rest" "spine101_8_IntProf" {
	for_each         = var.port-selector-36
	path             = "/api/node/mo/uni/infra/spaccportprof-spine101_IntProf/shports-Eth8-${each.value.name}-typ-range.json"
	class_name       = "infraSHPortS"
	payload          = <<EOF
{
    "infraSHPortS": {
        "attributes": {
            "dn": "uni/infra/spaccportprof-spine101_IntProf/shports-Eth8-${each.value.name}-typ-range",
            "name": "Eth8-${each.value.name}",
            "rn": "shports-Eth8-${each.value.name}-typ-range"
        },
        "children": [
            {
                "infraPortBlk": {
                    "attributes": {
                        "dn": "uni/infra/spaccportprof-spine101_IntProf/shports-Eth8-${each.value.name}-typ-range/portblk-block2",
                        "fromCard": "8",
                        "fromPort": "${each.value.name}",
                        "toCard": "8",
                        "toPort": "${each.value.name}",
                        "name": "block2",
                        "rn": "portblk-block2"
                    }
                }
            }
        ]
    }
}
	EOF
}

