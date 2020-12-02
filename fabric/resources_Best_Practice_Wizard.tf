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
				"coopPol": {
					"attributes": {
						"dn": "uni/fabric/pol-default",
						"rn": "pol-default",
						"type": "strict"
					},
					"children": []
				}
			},
			{
				"fabricNodeControl": {
					"attributes": {
						"dn": "uni/fabric/nodecontrol-default",
						"control": "1",
						"descr": "help my baby"
					},
					"children": []
				}
			},
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
				"l3IfPol": {
					"attributes": {
						"dn": "uni/fabric/l3IfP-default",
						"bfdIsis": "enabled",
						"descr": "Policy Enabled as part of the Brahma Startup Wizard"
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
						"enforceSubnetCheck": "true",
						"unicastXrEpLearnDisable": "true"
					},
					"children": []
				}
			},
			{
				"epControlP": {
					"attributes": {
						"dn": "uni/infra/epCtrlP-default",
						"adminSt": "enabled",
						"rogueEpDetectIntvl": "30",
						"rogueEpDetectMult": "6",
						"rn": "epCtrlP-default"
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
				"epLoopProtectP": {
					"attributes": {
						"dn": "uni/infra/epLoopProtectP-default",
						"adminSt": "enabled",
						"action": "",
						"rn": "epLoopProtectP-default"
					},
					"children": []
				}
			},
			{
				"infraPortTrackPol": {
					"attributes": {
						"dn": "uni/infra/trackEqptFabP-default",
						"adminSt": "on"
					},
					"children": []
				}
			},
			{
				"mcpInstPol": {
					"attributes": {
						"dn": "uni/infra/mcpInstP-default",
						"descr": "Policy Enabled as part of the Brahma Startup Wizard",
						"ctrl": "pdu-per-vlan",
						"adminSt": "enabled",
						"key": "cisco"
					},
					"children": []
				}
			},
			{
				"qosInstPol": {
					"attributes": {
						"dn": "uni/infra/qosinst-default",
						"ctrl": "dot1p-preserve"
					},
					"children": []
				}
			}
		]
	}
}
	EOF
}