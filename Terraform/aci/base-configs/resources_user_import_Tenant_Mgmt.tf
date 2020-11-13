# Use this Resource File to Register the inband management network for the Fabric

resource "aci_tenant" "mgmt" {
	name                   = "mgmt"
}

resource "aci_bridge_domain" "inb" {
	tenant_dn = aci_tenant.mgmt.id
	name                   = "inb"
}

resource "aci_subnet" "inb_subnet" {
	parent_dn              = aci_bridge_domain.inb.id
	ip                   = "192.168.87.254/24"
	scope                  = ["public"]
}

resource "aci_application_profile" "inb_ap" {
	tenant_dn              = aci_tenant.mgmt.id
	name                   = "inb_ap"
}

resource "aci_application_epg" "inb_epg" {
	application_profile_dn = aci_application_profile.inb_ap.id
	name                   = "inb_epg"
	description            = "Inband Mgmt EPG for APIC and Switch Management"
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

