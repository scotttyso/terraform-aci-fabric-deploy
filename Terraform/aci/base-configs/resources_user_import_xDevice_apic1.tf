resource "aci_rest" "inb_mgmt_apic_apic1" {
	path		= "/api/node/mo/uni/tn-mgmt.json"
	class_name	= "mgmtRsInBStNode"
	payload		= <<EOF
{
    "mgmtRsInBStNode": {
        "attributes": {
            "addr": "192.168.87.1/24",
            "dn": "uni/tn-mgmt/mgmtp-default/inb-inb_epg/rsinBStNode-[topology/pod-1/node-1]",
            "gw": "192.168.87.254",
            "tDn": "topology/pod-1/node-1"
        }
    }
}
	EOF
}

resource "aci_rest" "apic1_port_2_1" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf201_IntProf/hports-Eth1-48-typ-range/rsaccBaseGrp.json"
	class_name	= "infraRsAccBaseGrp"
	payload		= <<EOF
{
    "infraRsAccBaseGrp": {
        "attributes": {
            "tDn": "uni/infra/funcprof/accportgrp-inband_ap"
        }
    }
}
	EOF
}

resource "aci_rest" "apic1_port_2_2" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf202_IntProf/hports-Eth1-48-typ-range/rsaccBaseGrp.json"
	class_name	= "infraRsAccBaseGrp"
	payload		= <<EOF
{
    "infraRsAccBaseGrp": {
        "attributes": {
            "tDn": "uni/infra/funcprof/accportgrp-inband_ap"
        }
    }
}
	EOF
}

