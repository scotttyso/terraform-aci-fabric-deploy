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
            "addr": "192.168.85.12/24",
            "gw": "192.168.85.254",
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
            "dn": "uni/tn-mgmt/mgmtp-default/inb-inb_epg/rsinBStNode-[topology/pod-1/node-202]",
            "addr": "192.168.87.12/24",
            "gw": "192.168.87.254",
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

resource "aci_leaf_profile" "leaf202_SwSel" {
	name = "leaf202_SwSel"
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

resource "aci_leaf_interface_profile" "leaf202_IntProf" {
	name	= "leaf202_IntProf"
}

resource "aci_rest" "leaf_int_selector_leaf202_IntProf" {
	path		= "/api/node/mo/uni/infra/nprof-leaf202_SwSel.json"
	class_name	= "infraRsAccPortP"
	payload		= <<EOF
{
    "infraRsAccPortP": {
        "attributes": {
            "tDn": "uni/infra/accportprof-leaf202_IntProf"
        }
    }
}
	EOF
}

resource "aci_rest" "leaf202_1_IntProf" {
	for_each         = var.port-selector-48
	path             = "/api/node/mo/uni/infra/accportprof-leaf202_IntProf/hports-Eth1-${each.value.name}-typ-range.json"
	class_name       = "infraHPortS"
	payload          = <<EOF
{
    "infraHPortS": {
        "attributes": {
            "dn": "uni/infra/accportprof-leaf202_IntProf/hports-Eth1-${each.value.name}-typ-range",
            "name": "Eth1-${each.value.name}",
            "rn": "hports-Eth1-${each.value.name}-typ-range"
        },
        "children": [
            {
                "infraPortBlk": {
                    "attributes": {
                        "dn": "uni/infra/accportprof-leaf202_IntProf/hports-Eth1-${each.value.name}-typ-range/portblk-block2",
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

