resource "aci_rest" "snmp_cg" {
	for_each   = var.policies_snmp
	path       = "/api/node/mo/uni/fabric/snmppol-default/clgrp-${each.value.name}_Clients.json"
	class_name = "snmpClientGrpP"
	payload    = <<EOF
{
	"snmpClientGrpP": {
		"attributes": {
			"dn": "uni/fabric/snmppol-default/clgrp-${each.value.name}_Clients",
			"name": "${each.value.name}_Clients",
			"descr": "SNMP Clients allowed on ${each.value.name} Mgmt",
			"rn": "clgrp-${each.value.name}_Clients",
			"status": "created"
		},
		"children": [
			{
				"snmpRsEpg": {
					"attributes": {
						"tDn": "uni/tn-mgmt/mgmtp-default/${each.value.epg}",
						"status": "created"
					},
					"children": []
				}
			}
		]
	}
}
	EOF
}

# Assign the Default SNMP Monitoring Policy to the VRF's
# In the variables_vrf_snmp.tf File
resource "aci_rest" "vrf_snmp" {
	for_each   = var.snmp_vrf
	path       = "/api/node/mo/uni/tn-mgmt/ctx-${each.value.name}/rsCtxMonPol.json"
	class_name = "fvRsCtxMonPol"
	payload    = <<EOF
{
	"fvRsCtxMonPol": {
		"attributes": {
			"tnMonEPGPolName": "default",
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "snmp_trap_Src" {
	path       = "/api/node/mo/uni/fabric/moncommon/snmpsrc-SNMP_Src.json"
	class_name = "snmpSrc"
	payload    = <<EOF
{
	"snmpSrc": {
		"attributes": {
			"dn": "uni/fabric/moncommon/snmpsrc-SNMP_Src",
			"incl": "audits,events,faults",
			"name": "SNMP_Src",
			"rn": "snmpsrc-SNMP_Src",
		},
		"children": [
			{
				"snmpRsDestGroup": {
					"attributes": {
						"tDn": "uni/fabric/snmpgroup-SNMP-TRAP_dg",
					},
					"children": []
				}
			}
		]
	}
}
	EOF
}

