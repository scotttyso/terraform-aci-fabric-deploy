resource "aci_tenant" "mgmt" {
	name                   = "mgmt"
}

resource "aci_bridge_domain" "inb" {
	tenant_dn = aci_tenant.mgmt.id
	name                   = "inb"
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

resource "aci_contract" "mgmt_In_Ct" {
	tenant_dn   = aci_tenant.mgmt.id
	description = "Default Mgmt Contract"
	name        = "mgmt_In_Ct"
	scope       = "tenant"
	filter {
		  description = "Mgmt Traffic"
		  filter_entry {
				entry_description	= "Allow https"
			filter_entry_name   	= "https"
				d_from_port        	= "https"
				d_to_port	        = "https"
				ether_t             = "ipv4"
				prot            	= "tcp"
				stateful			= "yes"  
		  }
		  filter_entry {
				entry_description   = "Allow icmp"
			filter_entry_name   	= "icmp"
				d_from_port        	= "unspecified"
				d_to_port        	= "unspecified"
				ether_t             = "ipv4"
				prot           		= "icmp"
		  }
		  filter_entry {
				entry_description   = "Allow SNMP"
			filter_entry_name   	= "snmp"
				d_from_port        	= "161"
				d_to_port        	= "162"
				ether_t             = "ipv4"
				prot           		= "udp"
		  }
		  filter_entry {
				entry_description   = "Allow ssh"
			filter_entry_name   	= "ssh"
				d_from_port        	= "22"
				d_to_port        	= "22"
				ether_t             = "ipv4"
				prot           		= "tcp" 
				stateful			= "yes" 
		  }
		  filter_name  = "Mgmt_In_Flt"
	}
}

resource "aci_contract" "mgmt_Out_Ct" {
	tenant_dn   = aci_tenant.mgmt.id
	description = "Default Mgmt Contract Outbound"
	name        = "mgmt_Out_Ct"
	scope       = "tenant"
	filter {
		  description = "Mgmt Traffic Outbound"
		  filter_entry {
				entry_description	= "Allow All IP"
			filter_entry_name   	= "IPv4_and_IPv6"
				d_from_port        	= "unspecified"
				d_to_port        	= "unspecified"
				ether_t             = "ip"
				stateful			= "yes"  
		  }
		  filter_entry {
				entry_description   = "Allow icmp"
			filter_entry_name   	= "icmp"
				d_from_port        	= "unspecified"
				d_to_port        	= "unspecified"
				ether_t             = "ip"
				prot           		= "icmp"
		  }
		  filter_name  = "Mgmt_Out_Flt"
	}
}

resource "aci_contract_subject" "Mgmt_Out_Subj" {
	contract_dn					 = aci_contract.mgmt_Out_Ct.id
	name						 = "Mgmt_Out_Subj"
	relation_vz_rs_subj_filt_att = ["uni/tn-mgmt/flt-Mgmt_Out_Flt"]
	rev_flt_ports				 = "no"
}

resource "aci_epg_to_contract" "inb_epg_provider" {
    application_epg_dn = aci_application_epg.inb_epg.id
    contract_dn  = aci_contract.mgmt_In_Ct.id
    contract_type = "provider"
}

resource "aci_epg_to_contract" "inb_epg_consumer" {
    application_epg_dn = aci_application_epg.inb_epg.id
    contract_dn  = aci_contract.mgmt_Out_Ct.id
    contract_type = "consumer"
}

resource "aci_rest" "oob_mgmt_In_Ct" {
	path       = "/api/node/mo/uni/tn-mgmt/oobbrc-oob_mgmt_In_Ct.json"
	class_name = "vzOOBBrCP"
	payload    = <<EOF
{
	"vzOOBBrCP": {
		"attributes": {
			"dn": "uni/tn-mgmt/oobbrc-oob_mgmt_In_Ct",
			"name": "oob_mgmt_In_Ct",
			"scope": "tenant",
			"rn": "oobbrc-oob_mgmt_In_Ct",
			"status": "created"
		},
		"children": [
			{
				"vzSubj": {
					"attributes": {
						"dn": "uni/tn-mgmt/oobbrc-oob_mgmt_In_Ct/subj-oob_mgmt_In_Subj",
						"name": "oob_mgmt_In_Subj",
						"rn": "subj-oob_mgmt_In_Subj",
						"status": "created"
					},
					"children": [
						{
							"vzRsSubjFiltAtt": {
								"attributes": {
									"status": "created,modified",
									"tnVzFilterName": "Mgmt_In_Flt"
								},
								"children": []
							}
						}
					]
				}
			}
		]
	}
}
	EOF
}

resource "aci_rest" "oob_mgmt_Out_Ct" {
	path       = "/api/node/mo/uni/tn-mgmt/oobbrc-oob_mgmt_Out_Ct.json"
	class_name = "vzOOBBrCP"
	payload    = <<EOF
{
	"vzOOBBrCP": {
		"attributes": {
			"dn": "uni/tn-mgmt/oobbrc-oob_mgmt_Out_Ct",
			"name": "oob_mgmt_Out_Ct",
			"scope": "tenant",
			"rn": "oobbrc-oob_mgmt_Out_Ct",
			"status": "created"
		},
		"children": [
			{
				"vzSubj": {
					"attributes": {
						"dn": "uni/tn-mgmt/oobbrc-oob_mgmt_Out_Ct/subj-oob_mgmt_Out_Subj",
						"name": "oob_mgmt_Out_Subj",
						"rn": "subj-oob_mgmt_Out_Subj",
						"status": "created"
					},
					"children": [
						{
							"vzRsSubjFiltAtt": {
								"attributes": {
									"status": "created,modified",
									"tnVzFilterName": "Mgmt_Out_Flt"
								},
								"children": []
							}
						}
					]
				}
			}
		]
	}
}
	EOF
}
resource "aci_rest" "oob-default_In_Ct" {
	path       = "/api/node/mo/uni/tn-mgmt/mgmtp-default/oob-default.json"
	class_name = "mgmtRsOoBProv"
	payload    = <<EOF
{
	"mgmtRsOoBProv": {
		"attributes": {
			"tnVzOOBBrCPName": "oob_mgmt_In_Ct",
			"prio": "level1"
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "oob-default_Priority" {
	path       = "/api/node/mo/uni/tn-mgmt/mgmtp-default/oob-default.json"
	class_name = "mgmtOoB"
	payload    = <<EOF
{
	"mgmtOoB": {
		"attributes": {
			"dn": "uni/tn-mgmt/mgmtp-default/oob-default",
			"prio": "level1"
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "inb_epg_provided" {
	path       = "/api/node/mo/uni/tn-mgmt/mgmtp-default/inb-inb_epg.json"
	class_name = "fvRsProv"
	payload    = <<EOF
{
	"fvRsProv": {
		"attributes": {
			"tnVzBrCPName": "mgmt_In_Ct",
			"prio": "level1"
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "inb_epg_consumed" {
	path       = "/api/node/mo/uni/tn-mgmt/mgmtp-default/inb-inb_epg.json"
	class_name = "fvRsCons"
	payload    = <<EOF
{
	"fvRsCons": {
		"attributes": {
			"tnVzBrCPName": "mgmt_Out_Ct",
			"prio": "level1"
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "oob-default_Ext_Inst" {
	path       = "/api/node/mo/uni/tn-mgmt/extmgmt-default/instp-oob_ExtEpg.json"
	class_name = "mgmtInstP"
	payload    = <<EOF
{
	"mgmtInstP": {
		"attributes": {
			"dn": "uni/tn-mgmt/extmgmt-default/instp-oob_ExtEpg",
			"name": "oob_ExtEpg",
			"rn": "instp-oob_ExtEpg",
		},
		"children": [
			{
				"mgmtSubnet": {
					"attributes": {
						"dn": "uni/tn-mgmt/extmgmt-default/instp-oob_ExtEpg/subnet-[0.0.0.0/0]",
						"ip": "0.0.0.0/0",
						"rn": "subnet-[0.0.0.0/0]",
					},
					"children": []
				}
			},
			{
				"mgmtRsOoBCons": {
					"attributes": {
						"tnVzOOBBrCPName": "oob_mgmt_Out_Ct",
						"prio": "level1",
					},
					"children": []
				}
			}
		]
	}
}
	EOF
}
