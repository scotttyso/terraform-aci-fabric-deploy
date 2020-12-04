# This File will include Port Group Confgiuration and Mapping

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

resource "aci_access_port_block" "leaf201_Eth1-1-03_descr" {
	access_port_selector_dn    = "uni/infra/accportprof-leaf201/hports-Eth1-1-03-typ-range"
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

resource "aci_access_port_block" "leaf201_Eth1-1-04_descr" {
	access_port_selector_dn    = "uni/infra/accportprof-leaf201/hports-Eth1-1-04-typ-range"
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
