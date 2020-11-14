# Use this Resource File to Register the inband management network for the Fabric

resource "aci_subnet" "inb_subnet" {
	parent_dn              = aci_bridge_domain.inb.id
	ip                   = "192.168.87.254/24"
	scope                  = ["public"]
}

resource "aci_ranges" "inb_vlan" {
	vlan_pool_dn	= "uni/infra/vlanns-[inband_vl-pool]-static"
	_from		    = "vlan-100"
	to		        = "vlan-100"
}

resource "aci_rest" "inb_mgmt_default_epg" {
	path       = "/api/node/mo/uni/tn-mgmt/mgmtp-default/inb-inb_epg.json"
	class_name = "mgmtInB"
	payload    = <<EOF
{
	"mgmtInB": {
		"attributes": {
			"descr": "",
			"dn": "uni/tn-mgmt/mgmtp-default/inb-inb_epg",
			"encap": "vlan-100",
			"name": "inb_epg",
		},
		"children": [
			{
				"mgmtRsMgmtBD": {
					"attributes": {
						"tnFvBDName": "inb"
					}
				}
			}
		]
	}
}
	EOF
}

