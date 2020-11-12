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