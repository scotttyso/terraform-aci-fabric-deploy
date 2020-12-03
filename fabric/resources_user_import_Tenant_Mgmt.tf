# Use this Resource File to Register the inband management network for the Fabric

resource "aci_subnet" "inb_subnet" {
	parent_dn  = aci_bridge_domain.inb.id
	ip         = "198.18.2.1/24"
	scope      = ["public"]
}

resource "aci_ranges" "inb_vlan" {
	vlan_pool_dn   = "uni/infra/vlanns-[inband_vl-pool]-static"
	_from          = "vlan-100"
	to		        = "vlan-100"
}

resource "aci_rest" "inb_mgmt_default_epg" {
	depends_on		= [aci_vlan_pool.default]
	path		= "/api/node/mo/uni/tn-mgmt/mgmtp-default/inb-default.json"
	class_name	= "mgmtInB"
	payload		= <<EOF
{
    "mgmtInB": {
        "attributes": {
            "dn": "uni/tn-mgmt/mgmtp-default/inb-default",
            "descr": "Default Inband Mmgmt EPG Used by Brahma Startup Wizard.",
            "encap": "vlan-100",
            "name": "default"
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

