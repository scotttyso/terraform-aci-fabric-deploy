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

resource "aci_leaf_profile" "leaf201_SwSel" {
	name = "leaf201_SwSel"
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

resource "aci_leaf_interface_profile" "leaf201_IntProf" {
	name	= "leaf201_IntProf"
}

resource "aci_rest" "leaf_int_selector_leaf201_IntProf" {
	path		= "/api/node/mo/uni/infra/nprof-leaf201_SwSel.json"
	class_name	= "infraRsAccPortP"
	payload		= <<EOF
{
    "infraRsAccPortP": {
        "attributes": {
            "tDn": "uni/infra/accportprof-leaf201_IntProf"
        }
    }
}
	EOF
}

resource "aci_rest" "leaf_policy_group_leaf201_SwSel" {
	path		= "/api/node/mo/uni/infra/nprof-leaf201_SwSel/leaves-leaf201-typ-range.json"
	class_name	= "infraLeafS"
	payload		= <<EOF
{
    "infraLeafS": {
        "attributes": {
            "dn": "uni/infra/nprof-leaf201_SwSel/leaves-leaf201-typ-range"
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

resource "aci_rest" "leaf201_1_IntProf" {
	for_each         = var.port-selector-54
	path             = "/api/node/mo/uni/infra/accportprof-leaf201_IntProf/hports-Eth1-${each.value.name}-typ-range.json"
	class_name       = "infraHPortS"
	payload          = <<EOF
{
    "infraHPortS": {
        "attributes": {
            "dn": "uni/infra/accportprof-leaf201_IntProf/hports-Eth1-${each.value.name}-typ-range",
            "name": "Eth1-${each.value.name}",
            "rn": "hports-Eth1-${each.value.name}-typ-range"
        },
        "children": [
            {
                "infraPortBlk": {
                    "attributes": {
                        "dn": "uni/infra/accportprof-leaf201_IntProf/hports-Eth1-${each.value.name}-typ-range/portblk-block2",
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

