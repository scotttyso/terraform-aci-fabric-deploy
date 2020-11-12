resource "aci_contract" "mgmt_ctx" {
	tenant_dn   = aci_tenant.mgmt.id
	description = "Default Mgmt Contract"
	name        = "mgmt_ctx"
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
		  filter_name  = "Remote_Mgmt"
	}
}

resource "aci_contract_subject" "Mgmt_Subj" {
	contract_dn					 = aci_contract.mgmt_ctx.id
	name						 = "Mgmt_Subj"
	relation_vz_rs_subj_filt_att = ["uni/tn-mgmt/flt-Remote_Mgmt"]
	rev_flt_ports				 = "yes"
}

resource "aci_epg_to_contract" "inb-inb_epg" {
    application_epg_dn = aci_application_epg.inb_epg.id
    contract_dn  = aci_contract.mgmt_ctx.id
    contract_type = "provider"
}

resource "aci_rest" "oob_mgmt_ctx" {
	path       = "/api/node/mo/uni/tn-mgmt/oobbrc-oob_mgmt_ctx.json"
	class_name = "vzOOBBrCP"
	payload    = <<EOF
{
	"vzOOBBrCP": {
		"attributes": {
			"dn": "uni/tn-mgmt/oobbrc-oob_mgmt_ctx",
			"name": "oob_mgmt_ctx",
			"scope": "tenant",
			"rn": "oobbrc-oob_mgmt_ctx",
			"status": "created"
		},
		"children": [
			{
				"vzSubj": {
					"attributes": {
						"dn": "uni/tn-mgmt/oobbrc-oob_mgmt_ctx/subj-oob_mgmt_Subj",
						"name": "oob_mgmt_Subj",
						"rn": "subj-oob_mgmt_Subj",
						"status": "created"
					},
					"children": [
						{
							"vzRsSubjFiltAtt": {
								"attributes": {
									"status": "created,modified",
									"tnVzFilterName": "Remote_Mgmt"
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