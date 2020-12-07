# This File will include Port Group Confgiuration and Mapping

resource "aci_rest" "leaf201_Eth1-03_pg" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf201/hports-Eth1-03-typ-range/rsaccBaseGrp.json"
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

resource "aci_rest" "leaf201_Eth1-07_pg" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf201/hports-Eth1-07-typ-range/rsaccBaseGrp.json"
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

resource "aci_rest" "leaf202_Eth1-03_pg" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf202/hports-Eth1-03-typ-range/rsaccBaseGrp.json"
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

resource "aci_rest" "leaf202_Eth1-04_pg" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf202/hports-Eth1-04-typ-range/rsaccBaseGrp.json"
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

resource "aci_rest" "leaf202_Eth1-07_pg" {
	path		= "/api/node/mo/uni/infra/accportprof-leaf202/hports-Eth1-07-typ-range/rsaccBaseGrp.json"
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

