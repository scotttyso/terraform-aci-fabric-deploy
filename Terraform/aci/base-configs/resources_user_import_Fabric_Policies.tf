# This File will include DNS, Domain, NTP, Timezone and other base configuration parameters
resource "aci_rest" "bgp_as" {
	path       = "/api/node/mo/uni/fabric/bgpInstP-default/as.json"
	class_name = "bgpAsP"
	payload    = <<EOF
{
	"bgpAsP": {
		"attributes": {
			"dn": "uni/fabric/bgpInstP-default/as",
			"asn": "65535",
			"rn": "as"
		}
	}
}
	EOF
}

resource "aci_rest" "bgp_rr_101" {
	path       = "/api/node/mo/uni/fabric/bgpInstP-default/rr/node-101.json"
	class_name = "bgpRRNodePEp"
	payload    = <<EOF
{
	"bgpRRNodePEp": {
		"attributes": {
			"dn": "uni/fabric/bgpInstP-default/rr/node-101",
			"id": "101",
			"rn": "node-101"
		}
	}
}
	EOF
}

resource "aci_rest" "dns_mgmt" {
	path       = "/api/node/mo/uni/fabric/dnsp-default.json"
	class_name = "dnsRsProfileToEpg"
	payload    = <<EOF
{
	"dnsRsProfileToEpg": {
		"attributes": {
			"tDn": "uni/tn-mgmt/mgmtp-default/oob-default",
		}
	}
}
	EOF
}

resource "aci_rest" "dns_10_101_128_15" {
	path       = "/api/node/mo/uni/fabric/dnsp-default/prov-[10.101.128.15].json"
	class_name = "dnsProv"
	payload    = <<EOF
{
	"dnsProv": {
		"attributes": {
			"dn": "uni/fabric/dnsp-default/prov-[10.101.128.15]",
			"addr": "10.101.128.15",
			"preferred": "no",
			"rn": "prov-[10.101.128.15]"
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "dns_10_101_128_16" {
	path       = "/api/node/mo/uni/fabric/dnsp-default/prov-[10.101.128.16].json"
	class_name = "dnsProv"
	payload    = <<EOF
{
	"dnsProv": {
		"attributes": {
			"dn": "uni/fabric/dnsp-default/prov-[10.101.128.16]",
			"addr": "10.101.128.16",
			"preferred": "yes",
			"rn": "prov-[10.101.128.16]"
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "sched_CallHome" {
	path       = "/api/node/mo/uni/fabric/schedp-CallHome_scheduler.json"
	class_name = "trigSchedP"
	payload    = <<EOF
{
	"trigSchedP": {
		"attributes": {
			"dn": "uni/fabric/schedp-CallHome_scheduler",
			"name": "CallHome_scheduler",
			"descr": "CallHome_scheduler added by Brahma Startup Wizard",
			"rn": "schedp-CallHome_scheduler",
			"status": "created"
		},
		"children": [
			{
				"trigAbsWindowP": {
					"attributes": {
						"dn": "uni/fabric/schedp-CallHome_scheduler/abswinp-CallHome_onetime",
						"name": "CallHome_onetime",
						"date": "2020-11-14T16:06:32.855Z",
						"concurCap": "20",
						"rn": "abswinp-CallHome_onetime",
					},
					"children": []
				}
			},
			{
				"trigRecurrWindowP": {
					"attributes": {
						"dn": "uni/fabric/schedp-CallHome_scheduler/recurrwinp-CallHome_trigger",
						"name": "CallHome_trigger",
						"hour": "1",
						"concurCap": "20",
						"rn": "recurrwinp-CallHome_trigger",
					},
					"children": []
				}
			}
		]
	}
}
	EOF
}

resource "aci_rest" "CallHome_query" {
	path       = "/api/node/mo/uni/fabric/chquerygroup-CallHome_query.json"
	class_name = "callhomeQueryGroup"
	payload    = <<EOF
{
	"callhomeQueryGroup": {
		"attributes": {
			"dn": "uni/fabric/chquerygroup-CallHome_query",
			"name": "CallHome_query",
			"rn": "chquerygroup-CallHome_query",
		},
		"children": [
			{
				"callhomeQuery": {
					"attributes": {
						"dn": "uni/fabric/chquerygroup-CallHome_query/chquery-CallHome_query",
						"name": "CallHome_query",
						"target": "subtree",
						"rspSubtree": "full",
						"rspSubtreeInclude": "event-logs,count,stats,state,port-deployment,tasks,relations-with-parent,health,fault-count,local-prefix,config-only,record-subtree,no-scoped,relations,health-records,audit-logs,deployment,required,faults,fault-records",
						"rn": "chquery-CallHome_query",
					},
					"children": []
				}
			}
		]
	}
}
	EOF
}

resource "aci_rest" "SmartCallHome_dg" {
	path       = "/api/node/mo/uni/fabric/smartgroup-SmartCallHome_dg.json"
	class_name = "callhomeSmartGroup"
	payload    = <<EOF
{
	"callhomeSmartGroup": {
		"attributes": {
			"dn": "uni/fabric/smartgroup-SmartCallHome_dg",
			"name": "SmartCallHome_dg",
			"rn": "smartgroup-SmartCallHome_dg"
		},
		"children": [
			{
				"callhomeProf": {
					"attributes": {
						"dn": "uni/fabric/smartgroup-SmartCallHome_dg/prof",
						"port": "25",
						"from": "asgard-aci@rich.ciscolabs.com",
						"replyTo": "rich-lab@cisco.com",
						"email": "rich-lab@cisco.com",
						"phone": "+1-408-525-5300",
						"contact": "Richfield Labs",
						"addr": "4125 Highlander Pkwy_Richfield_OH 44286",
						"contract": "5555555",
						"customer": "5555555",
						"site": "555555",
						"rn": "prof"
					},
					"children": [
						{
							"callhomeSmtpServer": {
								"attributes": {
									"dn": "uni/fabric/smartgroup-SmartCallHome_dg/prof/smtp",
									"host": "cisco-ext.cisco.com",
									"rn": "smtp"
								},
								"children": [
									{
										"fileRsARemoteHostToEpg": {
											"attributes": {
												"tDn": "uni/tn-mgmt/mgmtp-default/oob-default",
											},
											"children": []
										}
									}
								]
							}
						}
					]
				}
			},
			{
				"callhomeSmartDest": {
					"attributes": {
						"dn": "uni/fabric/smartgroup-SmartCallHome_dg/smartdest-SCH_Receiver",
						"name": "SCH_Receiver",
						"email": "rich-lab@cisco.com",
						"format": "short-txt",
						"rn": "smartdest-SCH_Receiver"
					},
					"children": []
				}
			}
		]
	}
}
	EOF
}

resource "aci_rest" "CallHome_dg" {
	path       = "/api/node/mo/uni/fabric/chgroup-CallHome_dg.json"
	class_name = "callhomeGroup"
	payload    = <<EOF
{
	"callhomeGroup": {
		"attributes": {
			"dn": "uni/fabric/chgroup-CallHome_dg",
			"name": "CallHome_dg",
			"descr": "CallHome_dg added by Brahma Startup Wizard",
			"rn": "chgroup-CallHome_dg",
		},
		"children": [
			{
				"callhomeDest": {
					"attributes": {
						"dn": "uni/fabric/chgroup-CallHome_dg/dest-CallHome_dest",
						"name": "CallHome_dest",
						"email": "rich-lab@cisco.com",
						"format": "short-txt",
						"rn": "dest-CallHome_dest",
					},
					"children": []
				}
			},
			{
				"callhomeProf": {
					"attributes": {
						"dn": "uni/fabric/chgroup-CallHome_dg/prof",
						"port": "25",
						"from": "asgard-aci@rich.ciscolabs.com",
						"replyTo": "rich-lab@cisco.com",
						"email": "rich-lab@cisco.com",
						"phone": "+1-408-525-5300",
						"contact": "Richfield Labs",
						"addr": "4125 Highlander Pkwy_Richfield_OH 44286",
						"contract": "5555555",
						"customer": "5555555",
						"site": "555555",
						"rn": "prof",
					},
					"children": [
						{
							"callhomeSmtpServer": {
								"attributes": {
									"dn": "uni/fabric/chgroup-CallHome_dg/prof/smtp",
									"host": "cisco-ext.cisco.com",
									"rn": "smtp",
								},
								"children": [
									{
										"fileRsARemoteHostToEpg": {
											"attributes": {
												"tDn": "uni/tn-mgmt/mgmtp-default/oob-default",
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
		]
	}
}
	EOF
}

resource "aci_rest" "default_inventory" {
	path       = "/api/node/mo/uni/fabric/chinvp-default.json"
	class_name = "callhomeInvP"
	payload    = <<EOF
{
	"callhomeInvP": {
		"attributes": {
			"dn": "uni/fabric/chinvp-default",
			"name": "default",
			"maximumRetryCount": "3",
			"rn": "chinvp-default",
		},
		"children": [
			{
				"callhomeRsDestGroupRel": {
					"attributes": {
						"tDn": "uni/fabric/chgroup-CallHome_dg",
					},
					"children": []
				}
			},
			{
				"callhomeRsInvScheduler": {
					"attributes": {
						"tnTrigSchedPName": "CallHome_scheduler",
					},
					"children": []
				}
			}
		]
	}
}
	EOF
}

resource "aci_rest" "monfab_CallHome_src" {
	path       = "/api/node/mo/uni/fabric/monfab-default/chsrc-CallHome_src.json"
	class_name = "callhomeSrc"
	payload    = <<EOF
{
	"callhomeSrc": {
		"attributes": {
			"dn": "uni/fabric/monfab-default/chsrc-CallHome_src",
			"name": "CallHome_src",
			"incl": "events,audit,faults",
			"rn": "chsrc-CallHome_src",
		},
		"children": [
			{
				"callhomeRsDestGroup": {
					"attributes": {
						"tDn": "uni/fabric/chgroup-CallHome_dg",
					},
					"children": []
				}
			},
			{
				"callhomeRsQueryGroupRel": {
					"attributes": {
						"tDn": "uni/fabric/chquerygroup-CallHome_query",
					},
					"children": []
				}
			}
		]
	}
}
	EOF
}

resource "aci_rest" "moncommon_CallHome_src" {
	path       = "/api/node/mo/uni/fabric/moncommon/chsrc-CallHome_src.json"
	class_name = "callhomeSrc"
	payload    = <<EOF
{
	"callhomeSrc": {
		"attributes": {
			"dn": "uni/fabric/moncommon/chsrc-CallHome_src",
			"name": "CallHome_src",
			"incl": "events,audit,faults",
			"rn": "chsrc-CallHome_src",
		},
		"children": [
			{
				"callhomeRsDestGroup": {
					"attributes": {
						"tDn": "uni/fabric/chgroup-CallHome_dg",
					},
					"children": []
				}
			},
			{
				"callhomeRsQueryGroupRel": {
					"attributes": {
						"tDn": "uni/fabric/chquerygroup-CallHome_query",
					},
					"children": []
				}
			}
		]
	}
}
	EOF
}

resource "aci_rest" "moninfra_CallHome_src" {
	path       = "/api/node/mo/uni/infra/moninfra-default/chsrc-CallHome_src.json"
	class_name = "callhomeSrc"
	payload    = <<EOF
{
	"callhomeSrc": {
		"attributes": {
			"dn": "uni/infra/moninfra-default/chsrc-CallHome_src",
			"name": "CallHome_src",
			"incl": "events,audit,faults",
			"rn": "chsrc-CallHome_src",
		},
		"children": [
			{
				"callhomeRsDestGroup": {
					"attributes": {
						"tDn": "uni/fabric/chgroup-CallHome_dg",
					},
					"children": []
				}
			},
			{
				"callhomeRsQueryGroupRel": {
					"attributes": {
						"tDn": "uni/fabric/chquerygroup-CallHome_query",
					},
					"children": []
				}
			}
		]
	}
}
	EOF
}

resource "aci_rest" "ntp_192_168_64_39" {
	path       = "/api/node/mo/uni/fabric/time-default/ntpprov-192.168.64.39.json"
	class_name = "datetimeNtpProv"
	payload    = <<EOF
{
	"datetimeNtpProv": {
		"attributes": {
			"dn": "uni/fabric/time-default/ntpprov-192.168.64.39",
			"name": "192.168.64.39",
			"preferred": "true",
			"rn": "ntpprov-192.168.64.39",
		},
		"children": [
			{
				"datetimeRsNtpProvToEpg": {
					"attributes": {
						"tDn": "uni/tn-mgmt/mgmtp-default/oob-default",
					}
				}
			}
		]
	}
}
	EOF
}

resource "aci_rest" "ntp_10_101_128_15" {
	path       = "/api/node/mo/uni/fabric/time-default/ntpprov-10.101.128.15.json"
	class_name = "datetimeNtpProv"
	payload    = <<EOF
{
	"datetimeNtpProv": {
		"attributes": {
			"dn": "uni/fabric/time-default/ntpprov-10.101.128.15",
			"name": "10.101.128.15",
			"preferred": "false",
			"rn": "ntpprov-10.101.128.15",
		},
		"children": [
			{
				"datetimeRsNtpProvToEpg": {
					"attributes": {
						"tDn": "uni/tn-mgmt/mgmtp-default/oob-default",
					}
				}
			}
		]
	}
}
	EOF
}

resource "aci_rest" "domain_rich_ciscolabs_com" {
	path       = "/api/node/mo/uni/fabric/dnsp-default/dom-[rich.ciscolabs.com].json"
	class_name = "dnsDomain"
	payload    = <<EOF
{
	"dnsDomain": {
		"attributes": {
			"dn": "uni/fabric/dnsp-default/dom-[rich.ciscolabs.com]",
			"name": "rich.ciscolabs.com",
			"isDefault": "yes",
			"rn": "dom-[rich.ciscolabs.com]"
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "snmp_client_10_0_0_1" {
	path       = "/api/node/mo/uni/fabric/snmppol-default/clgrp-Out-of-Band_Clients/client-[10.0.0.1].json"
	class_name = "snmpClientP"
	payload    = <<EOF
{
	"snmpClientP": {
		"attributes": {
			"dn": "uni/fabric/snmppol-default/clgrp-Out-of-Band_Clients/client-[10.0.0.1]",
			"name": "snmp-server1",
			"addr": "10.0.0.1",
			"rn": "client-10.0.0.1",
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "snmp_client_10_0_0_2" {
	path       = "/api/node/mo/uni/fabric/snmppol-default/clgrp-Inband_Clients/client-[10.0.0.2].json"
	class_name = "snmpClientP"
	payload    = <<EOF
{
	"snmpClientP": {
		"attributes": {
			"dn": "uni/fabric/snmppol-default/clgrp-Inband_Clients/client-[10.0.0.2]",
			"name": "snmp-server2",
			"addr": "10.0.0.2",
			"rn": "client-10.0.0.2",
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "snmp_info" {
	path       = "/api/node/mo/uni/fabric/snmppol-default.json"
	class_name = "snmpPol"
	payload    = <<EOF
{
	"snmpPol": {
		"attributes": {
			"dn": "uni/fabric/snmppol-default",
			"descr": "This is the default SNMP Policy",
			"adminSt": "enabled",
			"contact": "rich-lab@cisco.com",
			"loc": "Richfield Ohio",
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "snmp_comm_read_access" {
	path       = "/api/node/mo/uni/fabric/snmppol-default/community-read_access.json"
	class_name = "snmpCommunityP"
	payload    = <<EOF
{
	"snmpCommunityP": {
		"attributes": {
			"dn": "uni/fabric/snmppol-default/community-read_access",
			"descr": "is it needed",
			"name": "read_access",
			"rn": "community-read_access"
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "snmp_comm_will-this-work" {
	path       = "/api/node/mo/uni/fabric/snmppol-default/community-will-this-work.json"
	class_name = "snmpCommunityP"
	payload    = <<EOF
{
	"snmpCommunityP": {
		"attributes": {
			"dn": "uni/fabric/snmppol-default/community-will-this-work",
			"descr": "",
			"name": "will-this-work",
			"rn": "community-will-this-work"
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "snmp_trap_default_10_0_0_1" {
	path       = "/api/node/mo/uni/fabric/snmppol-default/trapfwdserver-[10.0.0.1].json"
	class_name = "snmpTrapFwdServerP"
	payload    = <<EOF
{
	"snmpTrapFwdServerP": {
		"attributes": {
			"addr": "10.0.0.1",
			"port": "162",
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "snmp_trap_common_10_0_0_1" {
	path       = "/api/node/mo/uni/fabric/snmppol-default/trapfwdserver-[10.0.0.1].json"
	class_name = "snmpTrapFwdServerP"
	payload    = <<EOF
{
	"snmpTrapFwdServerP": {
		"attributes": {
			"addr": "10.0.0.1",
			"port": "162",
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "snmp_user_cisco_user1" {
	path       = "/api/node/mo/uni/fabric/snmppol-default/user-cisco_user1.json"
	class_name = "snmpUserP"
	payload    = <<EOF
{
	"snmpUserP": {
		"attributes": {
			"privType": "aes-128",
			"privKey": "cisco123",
			"authKey": "cisco123",
			"authType": "hmac-sha1-96",
			"name": "cisco_user1",
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "snmp_user_cisco_user2" {
	path       = "/api/node/mo/uni/fabric/snmppol-default/user-cisco_user2.json"
	class_name = "snmpUserP"
	payload    = <<EOF
{
	"snmpUserP": {
		"attributes": {
			"privType": "des",
			"privKey": "cisco123",
			"authKey": "cisco123",
			"name": "cisco_user2",
		},
		"children": []
	}
}
	EOF
}

resource "aci_rest" "snmp_user_cisco_user3" {
	path       = "/api/node/mo/uni/fabric/snmppol-default/user-cisco_user3.json"
	class_name = "snmpUserP"
	payload    = <<EOF
{
	"snmpUserP": {
		"attributes": {
			"authKey": "cisco123",
			"authType": "hmac-sha1-96",
			"name": "cisco_user3",
		},
		"children": []
	}
}
	EOF
}

