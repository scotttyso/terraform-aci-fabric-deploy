# This File will include DNS, Domain, NTP, SmartCallHome
# SNMP, Syslog and other base configuration parameters
resource "aci_rest" "encryption_key" {
	path		= "/api/node/mo/uni/exportcryptkey.json"
	class_name	= "pkiExportEncryptionKey"
	payload		= <<EOF
{
    "pkiExportEncryptionKey": {
        "attributes": {
            "dn": "uni/exportcryptkey",
            "strongEncryptionEnabled": "true",
            "passphrase": "cisco123cisco123"
        },
        "children": []
    }
}
	EOF
}

resource "aci_rest" "remote_location_lnx2.example.com" {
	path		= "/api/node/mo/uni/fabric/path-lnx2.example.com.json"
	class_name	= "fileRemotePath"
	payload		= <<EOF
{
    "fileRemotePath": {
        "attributes": {
            "dn": "uni/fabric/path-lnx2.example.com",
            "authType": "usePassword",
            "descr": "None",
            "host": "lnx2.example.com",
            "name": "lnx2.example.com",
            "protocol": "sftp",
            "remotePath": "/",
            "remotePort": "22",
            "userName": "username",
            "userPasswd": "cisco123",
            "rn": "path-lnx2.example.com"
        },
        "children": [
            {
                "fileRsARemoteHostToEpg": {
                    "attributes": {
                        "tDn": "uni/tn-mgmt/mgmtp-default/oob-default"
                    },
                    "children": []
                }
            }
        ]
    }
}
	EOF
}

resource "aci_rest" "backup_scheduler" {
	path		= "/api/node/mo/uni/fabric/schedp-Every24Hours.json"
	class_name	= "trigSchedP"
	payload		= <<EOF
{
    "trigSchedP": {
        "attributes": {
            "dn": "uni/fabric/schedp-Every24Hours",
            "name": "Every24Hours",
            "descr": "Create Backups Every 24 Hours - Brahma Startup Script.",
            "rn": "schedp-Every24Hours"
        },
        "children": [
            {
                "trigRecurrWindowP": {
                    "attributes": {
                        "dn": "uni/fabric/schedp-Every24Hours/recurrwinp-Every24Hours",
                        "name": "Every24Hours",
                        "hour": "0",
                        "minute": "0",
                        "concurCap": "20",
                        "rn": "recurrwinp-Every24Hours"
                    },
                    "children": []
                }
            }
        ]
    }
}
	EOF
}

resource "aci_rest" "backup_Policy" {
	path		= "/api/node/mo/uni/fabric/configexp-backup_every24Hours.json"
	class_name	= "configExportP"
	payload		= <<EOF
{
    "configExportP": {
        "attributes": {
            "dn": "uni/fabric/configexp-backup_every24Hours",
            "adminSt": "triggered",
            "name": "backup_every24Hours",
            "descr": "Backup Configuration Every 24 Hours - Created by Brahma Startup Script",
            "rn": "configexp-backup_every24Hours"
        },
        "children": [
            {
                "configRsExportScheduler": {
                    "attributes": {
                        "tnTrigSchedPName": "Every24Hours"
                    },
                    "children": []
                }
            },
            {
                "configRsRemotePath": {
                    "attributes": {
                        "tnFileRemotePathName": "lnx2.example.com"
                    },
                    "children": []
                }
            }
        ]
    }
}
	EOF
}

resource "aci_rest" "bgp_as_65513" {
	path		= "/api/node/mo/uni/fabric/bgpInstP-default/as.json"
	class_name	= "bgpAsP"
	payload		= <<EOF
{
    "bgpAsP": {
        "attributes": {
            "dn": "uni/fabric/bgpInstP-default/as",
            "asn": "65513",
            "rn": "as"
        },
        "children": []
    }
}
	EOF
}

resource "aci_rest" "bgp_rr_101" {
	path		= "/api/node/mo/uni/fabric/bgpInstP-default/rr/node-101.json"
	class_name	= "bgpRRNodePEp"
	payload		= <<EOF
{
    "bgpRRNodePEp": {
        "attributes": {
            "dn": "uni/fabric/bgpInstP-default/rr/node-101",
            "id": "101",
            "rn": "node-101"
        },
        "children": []
    }
}
	EOF
}

resource "aci_rest" "dns_epg_oob-default" {
	path		= "/api/node/mo/uni/fabric/dnsp-default.json"
	class_name	= "dnsRsProfileToEpg"
	payload		= <<EOF
{
    "dnsRsProfileToEpg": {
        "attributes": {
            "tDn": "uni/tn-mgmt/mgmtp-default/oob-default"
        },
        "children": []
    }
}
	EOF
}

resource "aci_rest" "dns_198_18_1_51" {
	path		= "/api/node/mo/uni/fabric/dnsp-default/prov-[198.18.1.51].json"
	class_name	= "dnsProv"
	payload		= <<EOF
{
    "dnsProv": {
        "attributes": {
            "dn": "uni/fabric/dnsp-default/prov-[198.18.1.51]",
            "addr": "198.18.1.51",
            "preferred": "no",
            "rn": "prov-[198.18.1.51]"
        },
        "children": []
    }
}
	EOF
}

resource "aci_rest" "dns_198_18_1_52" {
	path		= "/api/node/mo/uni/fabric/dnsp-default/prov-[198.18.1.52].json"
	class_name	= "dnsProv"
	payload		= <<EOF
{
    "dnsProv": {
        "attributes": {
            "dn": "uni/fabric/dnsp-default/prov-[198.18.1.52]",
            "addr": "198.18.1.52",
            "preferred": "yes",
            "rn": "prov-[198.18.1.52]"
        },
        "children": []
    }
}
	EOF
}

resource "aci_rest" "SmartCallHome_dg" {
	path		= "/api/node/mo/uni/fabric/smartgroup-SmartCallHome_dg.json"
	class_name	= "callhomeSmartGroup"
	payload		= <<EOF
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
                        "from": "cust-aci-fabric@example.com",
                        "replyTo": "network-ops@example.com",
                        "email": "network-ops@example.com",
                        "phone": "+1 408-555-5555",
                        "contact": "Brahma Lab",
                        "addr": "5555 Some Streat Some City, CA 95000",
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
                                    "host": "cisco-smtp.example.com",
                                    "rn": "smtp"
                                },
                                "children": [
                                    {
                                        "fileRsARemoteHostToEpg": {
                                            "attributes": {
                                                "tDn": "uni/tn-mgmt/mgmtp-default/oob-default"
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
                        "email": "network-ops@example.com",
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

resource "aci_rest" "callhomeSmartSrc" {
	path		= "/api/node/mo/uni/infra/moninfra-default/smartchsrc.json"
	class_name	= "callhomeSmartSrc"
	payload		= <<EOF
{
    "callhomeSmartSrc": {
        "attributes": {
            "dn": "uni/infra/moninfra-default/smartchsrc",
            "rn": "smartchsrc"
        },
        "children": [
            {
                "callhomeRsSmartdestGroup": {
                    "attributes": {
                        "tDn": "uni/fabric/smartgroup-SmartCallHome_dg"
                    },
                    "children": []
                }
            }
        ]
    }
}
	EOF
}

resource "aci_rest" "ntp_198_18_1_51" {
	path		= "/api/node/mo/uni/fabric/time-default/ntpprov-198.18.1.51.json"
	class_name	= "datetimeNtpProv"
	payload		= <<EOF
{
    "datetimeNtpProv": {
        "attributes": {
            "dn": "uni/fabric/time-default/ntpprov-198.18.1.51",
            "name": "198.18.1.51",
            "preferred": "false",
            "rn": "ntpprov-198.18.1.51"
        },
        "children": [
            {
                "datetimeRsNtpProvToEpg": {
                    "attributes": {
                        "tDn": "uni/tn-mgmt/mgmtp-default/oob-default"
                    }
                }
            }
        ]
    }
}
	EOF
}

resource "aci_rest" "ntp_198_18_1_52" {
	path		= "/api/node/mo/uni/fabric/time-default/ntpprov-198.18.1.52.json"
	class_name	= "datetimeNtpProv"
	payload		= <<EOF
{
    "datetimeNtpProv": {
        "attributes": {
            "dn": "uni/fabric/time-default/ntpprov-198.18.1.52",
            "name": "198.18.1.52",
            "preferred": "true",
            "rn": "ntpprov-198.18.1.52"
        },
        "children": [
            {
                "datetimeRsNtpProvToEpg": {
                    "attributes": {
                        "tDn": "uni/tn-mgmt/mgmtp-default/oob-default"
                    }
                }
            }
        ]
    }
}
	EOF
}

resource "aci_rest" "domain_rich_ciscolabs_com" {
	path		= "/api/node/mo/uni/fabric/dnsp-default/dom-[rich.ciscolabs.com].json"
	class_name	= "dnsDomain"
	payload		= <<EOF
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

resource "aci_rest" "domain_cisco_com" {
	path		= "/api/node/mo/uni/fabric/dnsp-default/dom-[cisco.com].json"
	class_name	= "dnsDomain"
	payload		= <<EOF
{
    "dnsDomain": {
        "attributes": {
            "dn": "uni/fabric/dnsp-default/dom-[cisco.com]",
            "name": "cisco.com",
            "isDefault": "no",
            "rn": "dom-[cisco.com]"
        },
        "children": []
    }
}
	EOF
}

resource "aci_rest" "snmp_client_198_18_1_61" {
	path		= "/api/node/mo/uni/fabric/snmppol-default/clgrp-Out-of-Band_Clients/client-[198.18.1.61].json"
	class_name	= "snmpClientP"
	payload		= <<EOF
{
    "snmpClientP": {
        "attributes": {
            "dn": "uni/fabric/snmppol-default/clgrp-Out-of-Band_Clients/client-[198.18.1.61]",
            "name": "snmp-server1",
            "addr": "198.18.1.61",
            "rn": "client-198.18.1.61"
        },
        "children": []
    }
}
	EOF
}

resource "aci_rest" "snmp_client_198_18_1_62" {
	path		= "/api/node/mo/uni/fabric/snmppol-default/clgrp-Out-of-Band_Clients/client-[198.18.1.62].json"
	class_name	= "snmpClientP"
	payload		= <<EOF
{
    "snmpClientP": {
        "attributes": {
            "dn": "uni/fabric/snmppol-default/clgrp-Out-of-Band_Clients/client-[198.18.1.62]",
            "name": "snmp-server2",
            "addr": "198.18.1.62",
            "rn": "client-198.18.1.62"
        },
        "children": []
    }
}
	EOF
}

resource "aci_rest" "snmp_info" {
	path		= "/api/node/mo/uni/fabric/snmppol-default.json"
	class_name	= "snmpPol"
	payload		= <<EOF
{
    "snmpPol": {
        "attributes": {
            "dn": "uni/fabric/snmppol-default",
            "descr": "This is the default SNMP Policy",
            "adminSt": "enabled",
            "contact": "rich-lab@cisco.com",
            "loc": "Richfield Ohio"
        },
        "children": []
    }
}
	EOF
}

resource "aci_rest" "snmp_comm_read_access" {
	path		= "/api/node/mo/uni/fabric/snmppol-default/community-read_access.json"
	class_name	= "snmpCommunityP"
	payload		= <<EOF
{
    "snmpCommunityP": {
        "attributes": {
            "dn": "uni/fabric/snmppol-default/community-read_access",
            "descr": "is it needed, I don't know",
            "name": "read_access",
            "rn": "community-read_access"
        },
        "children": []
    }
}
	EOF
}

resource "aci_rest" "snmp_comm_will-this-work" {
	path		= "/api/node/mo/uni/fabric/snmppol-default/community-will-this-work.json"
	class_name	= "snmpCommunityP"
	payload		= <<EOF
{
    "snmpCommunityP": {
        "attributes": {
            "dn": "uni/fabric/snmppol-default/community-will-this-work",
            "descr": "None",
            "name": "will-this-work",
            "rn": "community-will-this-work"
        },
        "children": []
    }
}
	EOF
}

resource "aci_rest" "snmp_trap_default_198_18_1_61" {
	path		= "/api/node/mo/uni/fabric/snmppol-default/trapfwdserver-[198.18.1.61].json"
	class_name	= "snmpTrapFwdServerP"
	payload		= <<EOF
{
    "snmpTrapFwdServerP": {
        "attributes": {
            "dn": "uni/fabric/snmppol-default/trapfwdserver-[198.18.1.61]",
            "addr": "198.18.1.61",
            "port": "162"
        },
        "children": []
    }
}
	EOF
}

resource "aci_rest" "snmp_trap_dest_198_18_1_61" {
	path		= "/api/node/mo/uni/fabric/snmpgroup-SNMP-TRAP_dg.json"
	class_name	= "snmpGroup"
	payload		= <<EOF
{
    "snmpGroup": {
        "attributes": {
            "dn": "uni/fabric/snmpgroup-SNMP-TRAP_dg",
            "descr": "SNMP Trap Destination Group - Created by Brahma Startup Script",
            "name": "SNMP-TRAP_dg",
            "rn": "snmpgroup-SNMP-TRAP_dg"
        },
        "children": [
            {
                "snmpTrapDest": {
                    "attributes": {
                        "dn": "uni/fabric/snmpgroup-SNMP-TRAP_dg/trapdest-198.18.1.61-port-162",
                        "ver": "v2c",
                        "host": "198.18.1.61",
                        "port": "162",
                        "secName": "read_access",
                        "v3SecLvl": "noauth",
                        "rn": "trapdest-198.18.1.61-port-162"
                    },
                    "children": [
                        {
                            "fileRsARemoteHostToEpg": {
                                "attributes": {
                                    "tDn": "uni/tn-mgmt/mgmtp-default/oob-default"
                                }
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

resource "aci_rest" "snmp_trap_default_198_18_1_62" {
	path		= "/api/node/mo/uni/fabric/snmppol-default/trapfwdserver-[198.18.1.62].json"
	class_name	= "snmpTrapFwdServerP"
	payload		= <<EOF
{
    "snmpTrapFwdServerP": {
        "attributes": {
            "dn": "uni/fabric/snmppol-default/trapfwdserver-[198.18.1.62]",
            "addr": "198.18.1.62",
            "port": "162"
        },
        "children": []
    }
}
	EOF
}

resource "aci_rest" "snmp_trap_dest_198_18_1_62" {
	path		= "/api/node/mo/uni/fabric/snmpgroup-SNMP-TRAP_dg.json"
	class_name	= "snmpGroup"
	payload		= <<EOF
{
    "snmpGroup": {
        "attributes": {
            "dn": "uni/fabric/snmpgroup-SNMP-TRAP_dg",
            "descr": "SNMP Trap Destination Group - Created by Brahma Startup Script",
            "name": "SNMP-TRAP_dg",
            "rn": "snmpgroup-SNMP-TRAP_dg"
        },
        "children": [
            {
                "snmpTrapDest": {
                    "attributes": {
                        "dn": "uni/fabric/snmpgroup-SNMP-TRAP_dg/trapdest-198.18.1.62-port-162",
                        "ver": "v3",
                        "host": "198.18.1.62",
                        "port": "162",
                        "secName": "cisco_user1",
                        "v3SecLvl": "priv",
                        "rn": "trapdest-198.18.1.62-port-162"
                    },
                    "children": [
                        {
                            "fileRsARemoteHostToEpg": {
                                "attributes": {
                                    "tDn": "uni/tn-mgmt/mgmtp-default/oob-default"
                                }
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

resource "aci_rest" "snmp_user_cisco_user1" {
	path		= "/api/node/mo/uni/fabric/snmppol-default/user-cisco_user1.json"
	class_name	= "snmpUserP"
	payload		= <<EOF
{
    "snmpUserP": {
        "attributes": {
            "dn": "uni/fabric/snmppol-default/user-cisco_user1",
            "name": "cisco_user1",
            "privType": "aes-128",
            "privKey": "cisco123",
            "authType": "hmac-sha1-96",
            "authKey": "cisco123"
        },
        "children": []
    }
}
	EOF
}

resource "aci_rest" "snmp_user_cisco_user2" {
	path		= "/api/node/mo/uni/fabric/snmppol-default/user-cisco_user2.json"
	class_name	= "snmpUserP"
	payload		= <<EOF
{
    "snmpUserP": {
        "attributes": {
            "dn": "uni/fabric/snmppol-default/user-cisco_user2",
            "name": "cisco_user2",
            "privType": "des",
            "privKey": "cisco123",
            "authKey": "cisco123"
        },
        "children": []
    }
}
	EOF
}

resource "aci_rest" "snmp_user_cisco_user3" {
	path		= "/api/node/mo/uni/fabric/snmppol-default/user-cisco_user3.json"
	class_name	= "snmpUserP"
	payload		= <<EOF
{
    "snmpUserP": {
        "attributes": {
            "dn": "uni/fabric/snmppol-default/user-cisco_user3",
            "name": "cisco_user3",
            "authType": "hmac-sha1-96",
            "authKey": "cisco123"
        },
        "children": []
    }
}
	EOF
}

resource "aci_rest" "syslog_198_18_1_61" {
	path		= "/api/node/mo/uni/fabric/slgroup-Syslog-dg_198.18.1.61.json"
	class_name	= "syslogGroup"
	payload		= <<EOF
{
    "syslogGroup": {
        "attributes": {
            "dn": "uni/fabric/slgroup-Syslog-dg_198.18.1.61",
            "includeMilliSeconds": "true",
            "includeTimeZone": "true",
            "descr": "Syslog Destination Group 198.18.1.61 - Created by Brahma Startup Wizard",
            "name": "Syslog-dg_198.18.1.61",
            "rn": "slgroup-Syslog-dg_198.18.1.61"
        },
        "children": [
            {
                "syslogConsole": {
                    "attributes": {
                        "dn": "uni/fabric/slgroup-Syslog-dg_198.18.1.61/console",
                        "adminState": "enabled",
                        "severity": "critical",
                        "rn": "console"
                    },
                    "children": []
                }
            },
            {
                "syslogFile": {
                    "attributes": {
                        "dn": "uni/fabric/slgroup-Syslog-dg_198.18.1.61/file",
                        "adminState": "enabled",
                        "severity": "information",
                        "rn": "file"
                    },
                    "children": []
                }
            },
            {
                "syslogProf": {
                    "attributes": {
                        "dn": "uni/fabric/slgroup-Syslog-dg_198.18.1.61/prof",
                        "adminState": "enabled",
                        "rn": "prof"
                    },
                    "children": []
                }
            },
            {
                "syslogRemoteDest": {
                    "attributes": {
                        "dn": "uni/fabric/slgroup-Syslog-dg_198.18.1.61/rdst-198.18.1.61",
                        "host": "198.18.1.61",
                        "name": "RmtDst-198.18.1.61",
                        "adminState": "enabled",
                        "forwardingFacility": "local7",
                        "port": "514",
                        "severity": "warnings",
                        "rn": "rdst-198.18.1.61"
                    },
                    "children": [
                        {
                            "fileRsARemoteHostToEpg": {
                                "attributes": {
                                    "tDn": "uni/tn-mgmt/mgmtp-default/oob-default"
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

resource "aci_rest" "aaaRadiusProvider_198_18_1_71" {
	path		= "/api/node/mo/uni/userext/radiusext/radiusprovider-198.18.1.71.json"
	class_name	= "aaaRadiusProvider"
	payload		= <<EOF
{
    "aaaRadiusProvider": {
        "attributes": {
            "dn": "uni/userext/radiusext/radiusprovider-198.18.1.71",
            "timeout": "5",
            "retries": "5",
            "monitorServer": "disabled",
            "key": "cisco1231",
            "authProtocol": "pap",
            "name": "198.18.1.71",
            "descr": "RADIUS Provider - 198.18.1.71.  Added by Brahma Startup Wizard.",
            "rn": "radiusprovider-198.18.1.71"
        },
        "children": [
            {
                "aaaRsSecProvToEpg": {
                    "attributes": {
                        "tDn": "uni/tn-mgmt/mgmtp-default/oob-default"
                    },
                    "children": []
                }
            }
        ]
    }
}
	EOF
}

resource "aci_rest" "Ext_Login_RADIUS_prov-198_18_1_71" {
	path		= "/api/node/mo/uni/userext.json"
	class_name	= "aaaUserEp"
	payload		= <<EOF
{
    "aaaUserEp": {
        "attributes": {
            "dn": "uni/userext"
        },
        "children": [
            {
                "aaaLoginDomain": {
                    "attributes": {
                        "dn": "uni/userext/logindomain-RAD_ISE",
                        "name": "RAD_ISE",
                        "rn": "logindomain-RAD_ISE"
                    },
                    "children": [
                        {
                            "aaaDomainAuth": {
                                "attributes": {
                                    "dn": "uni/userext/logindomain-RAD_ISE/domainauth",
                                    "providerGroup": "RAD_ISE",
                                    "realm": "radius",
                                    "descr": "RADIUS Login Domain RAD_ISE. Created by Brahma Wizard.",
                                    "rn": "domainauth"
                                },
                                "children": []
                            }
                        }
                    ]
                }
            },
            {
                "aaaRadiusEp": {
                    "attributes": {
                        "dn": "uni/userext/radiusext"
                    },
                    "children": [
                        {
                            "aaaRadiusProviderGroup": {
                                "attributes": {
                                    "dn": "uni/userext/radiusext/radiusprovidergroup-RAD_ISE"
                                },
                                "children": [
                                    {
                                        "aaaProviderRef": {
                                            "attributes": {
                                                "dn": "uni/userext/radiusext/radiusprovidergroup-RAD_ISE/providerref-198.18.1.71",
                                                "order": "1",
                                                "name": "198.18.1.71",
                                                "descr": "Added RADIUS Server 198.18.1.71 - Brahma Startup Wizard"
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

resource "aci_rest" "aaaRadiusProvider_198_18_1_72" {
	path		= "/api/node/mo/uni/userext/radiusext/radiusprovider-198.18.1.72.json"
	class_name	= "aaaRadiusProvider"
	payload		= <<EOF
{
    "aaaRadiusProvider": {
        "attributes": {
            "dn": "uni/userext/radiusext/radiusprovider-198.18.1.72",
            "timeout": "5",
            "retries": "5",
            "monitorServer": "disabled",
            "key": "cisco123",
            "authProtocol": "pap",
            "name": "198.18.1.72",
            "descr": "RADIUS Provider - 198.18.1.72.  Added by Brahma Startup Wizard.",
            "rn": "radiusprovider-198.18.1.72"
        },
        "children": [
            {
                "aaaRsSecProvToEpg": {
                    "attributes": {
                        "tDn": "uni/tn-mgmt/mgmtp-default/oob-default"
                    },
                    "children": []
                }
            }
        ]
    }
}
	EOF
}

resource "aci_rest" "Ext_Login_RADIUS_prov-198_18_1_72" {
	path		= "/api/node/mo/uni/userext.json"
	class_name	= "aaaUserEp"
	payload		= <<EOF
{
    "aaaUserEp": {
        "attributes": {
            "dn": "uni/userext"
        },
        "children": [
            {
                "aaaLoginDomain": {
                    "attributes": {
                        "dn": "uni/userext/logindomain-RAD_ISE",
                        "name": "RAD_ISE",
                        "rn": "logindomain-RAD_ISE"
                    },
                    "children": [
                        {
                            "aaaDomainAuth": {
                                "attributes": {
                                    "dn": "uni/userext/logindomain-RAD_ISE/domainauth",
                                    "providerGroup": "RAD_ISE",
                                    "realm": "radius",
                                    "descr": "RADIUS Login Domain RAD_ISE. Created by Brahma Wizard.",
                                    "rn": "domainauth"
                                },
                                "children": []
                            }
                        }
                    ]
                }
            },
            {
                "aaaRadiusEp": {
                    "attributes": {
                        "dn": "uni/userext/radiusext"
                    },
                    "children": [
                        {
                            "aaaRadiusProviderGroup": {
                                "attributes": {
                                    "dn": "uni/userext/radiusext/radiusprovidergroup-RAD_ISE"
                                },
                                "children": [
                                    {
                                        "aaaProviderRef": {
                                            "attributes": {
                                                "dn": "uni/userext/radiusext/radiusprovidergroup-RAD_ISE/providerref-198.18.1.72",
                                                "order": "2",
                                                "name": "198.18.1.72",
                                                "descr": "Added RADIUS Server 198.18.1.72 - Brahma Startup Wizard"
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

resource "aci_rest" "tacacs_TACACS_acct_198_18_1_71" {
	path		= "/api/node/mo/uni/fabric/tacacsgroup-TACACS_acct.json"
	class_name	= "tacacsGroup"
	payload		= <<EOF
{
    "tacacsGroup": {
        "attributes": {
            "dn": "uni/fabric/tacacsgroup-TACACS_acct",
            "descr": "TACACS Accounting Group TACACS_acct - Created by Brahma Startup Wizard",
            "name": "TACACS_acct",
            "rn": "tacacsgroup-TACACS_acct"
        },
        "children": [
            {
                "tacacsTacacsDest": {
                    "attributes": {
                        "dn": "uni/fabric/tacacsgroup-TACACS_acct/tacacsdest-198.18.1.71-port-49",
                        "authProtocol": "pap",
                        "host": "198.18.1.71",
                        "key": "cisco1231",
                        "rn": "tacacsdest-198.18.1.71-port-49"
                    },
                    "children": [
                        {
                            "fileRsARemoteHostToEpg": {
                                "attributes": {
                                    "tDn": "uni/tn-mgmt/mgmtp-default/oob-default"
                                }
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

resource "aci_rest" "tacacsSrc" {
	path		= "/api/node/mo/uni/fabric/moncommon/tacacssrc-TACACS_Src.json"
	class_name	= "tacacsSrc"
	payload		= <<EOF
{
    "tacacsSrc": {
        "attributes": {
            "dn": "uni/fabric/moncommon/tacacssrc-TACACS_Src",
            "name": "TACACS_Src",
            "rn": "tacacssrc-TACACS_Src"
        },
        "children": [
            {
                "tacacsRsDestGroup": {
                    "attributes": {
                        "tDn": "uni/fabric/tacacsgroup-TACACS_acct"
                    },
                    "children": []
                }
            }
        ]
    }
}
	EOF
}

resource "aci_rest" "aaaTacacsPlusProvider_198_18_1_71" {
	path		= "/api/node/mo/uni/userext/tacacsext/tacacsplusprovider-198.18.1.71.json"
	class_name	= "aaaTacacsPlusProvider"
	payload		= <<EOF
{
    "aaaTacacsPlusProvider": {
        "attributes": {
            "dn": "uni/userext/tacacsext/tacacsplusprovider-198.18.1.71",
            "timeout": "5",
            "retries": "5",
            "monitorServer": "disabled",
            "key": "cisco1231",
            "authProtocol": "pap",
            "name": "198.18.1.71",
            "descr": "TACACS+ Provider - 198.18.1.71.  Added by Brahma Startup Wizard.",
            "rn": "tacacsplusprovider-198.18.1.71"
        },
        "children": [
            {
                "aaaRsSecProvToEpg": {
                    "attributes": {
                        "tDn": "uni/tn-mgmt/mgmtp-default/oob-default"
                    },
                    "children": []
                }
            }
        ]
    }
}
	EOF
}

resource "aci_rest" "Ext_Login_TACACS_prov-198_18_1_71" {
	path		= "/api/node/mo/uni/userext.json"
	class_name	= "aaaUserEp"
	payload		= <<EOF
{
    "aaaUserEp": {
        "attributes": {
            "dn": "uni/userext"
        },
        "children": [
            {
                "aaaLoginDomain": {
                    "attributes": {
                        "dn": "uni/userext/logindomain-ISE",
                        "name": "ISE",
                        "rn": "logindomain-ISE"
                    },
                    "children": [
                        {
                            "aaaDomainAuth": {
                                "attributes": {
                                    "dn": "uni/userext/logindomain-ISE/domainauth",
                                    "providerGroup": "ISE",
                                    "realm": "tacacs",
                                    "descr": "TACACS+ Login Domain ISE. Created by Brahma Wizard.",
                                    "rn": "domainauth"
                                },
                                "children": []
                            }
                        }
                    ]
                }
            },
            {
                "aaaTacacsPlusEp": {
                    "attributes": {
                        "dn": "uni/userext/tacacsext"
                    },
                    "children": [
                        {
                            "aaaTacacsPlusProviderGroup": {
                                "attributes": {
                                    "dn": "uni/userext/tacacsext/tacacsplusprovidergroup-ISE"
                                },
                                "children": [
                                    {
                                        "aaaProviderRef": {
                                            "attributes": {
                                                "dn": "uni/userext/tacacsext/tacacsplusprovidergroup-ISE/providerref-198.18.1.71",
                                                "order": "1",
                                                "name": "198.18.1.71",
                                                "descr": "Added TACACS Server 198.18.1.71 - Brahma Startup Wizard"
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

resource "aci_rest" "tacacs_TACACS_acct_198_18_1_72" {
	path		= "/api/node/mo/uni/fabric/tacacsgroup-TACACS_acct.json"
	class_name	= "tacacsGroup"
	payload		= <<EOF
{
    "tacacsGroup": {
        "attributes": {
            "dn": "uni/fabric/tacacsgroup-TACACS_acct",
            "descr": "TACACS Accounting Group TACACS_acct - Created by Brahma Startup Wizard",
            "name": "TACACS_acct",
            "rn": "tacacsgroup-TACACS_acct"
        },
        "children": [
            {
                "tacacsTacacsDest": {
                    "attributes": {
                        "dn": "uni/fabric/tacacsgroup-TACACS_acct/tacacsdest-198.18.1.72-port-49",
                        "authProtocol": "pap",
                        "host": "198.18.1.72",
                        "key": "cisco123",
                        "rn": "tacacsdest-198.18.1.72-port-49"
                    },
                    "children": [
                        {
                            "fileRsARemoteHostToEpg": {
                                "attributes": {
                                    "tDn": "uni/tn-mgmt/mgmtp-default/oob-default"
                                }
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

resource "aci_rest" "aaaTacacsPlusProvider_198_18_1_72" {
	path		= "/api/node/mo/uni/userext/tacacsext/tacacsplusprovider-198.18.1.72.json"
	class_name	= "aaaTacacsPlusProvider"
	payload		= <<EOF
{
    "aaaTacacsPlusProvider": {
        "attributes": {
            "dn": "uni/userext/tacacsext/tacacsplusprovider-198.18.1.72",
            "timeout": "5",
            "retries": "5",
            "monitorServer": "disabled",
            "key": "cisco123",
            "authProtocol": "pap",
            "name": "198.18.1.72",
            "descr": "TACACS+ Provider - 198.18.1.72.  Added by Brahma Startup Wizard.",
            "rn": "tacacsplusprovider-198.18.1.72"
        },
        "children": [
            {
                "aaaRsSecProvToEpg": {
                    "attributes": {
                        "tDn": "uni/tn-mgmt/mgmtp-default/oob-default"
                    },
                    "children": []
                }
            }
        ]
    }
}
	EOF
}

resource "aci_rest" "Ext_Login_TACACS_prov-198_18_1_72" {
	path		= "/api/node/mo/uni/userext.json"
	class_name	= "aaaUserEp"
	payload		= <<EOF
{
    "aaaUserEp": {
        "attributes": {
            "dn": "uni/userext"
        },
        "children": [
            {
                "aaaLoginDomain": {
                    "attributes": {
                        "dn": "uni/userext/logindomain-ISE",
                        "name": "ISE",
                        "rn": "logindomain-ISE"
                    },
                    "children": [
                        {
                            "aaaDomainAuth": {
                                "attributes": {
                                    "dn": "uni/userext/logindomain-ISE/domainauth",
                                    "providerGroup": "ISE",
                                    "realm": "tacacs",
                                    "descr": "TACACS+ Login Domain ISE. Created by Brahma Wizard.",
                                    "rn": "domainauth"
                                },
                                "children": []
                            }
                        }
                    ]
                }
            },
            {
                "aaaTacacsPlusEp": {
                    "attributes": {
                        "dn": "uni/userext/tacacsext"
                    },
                    "children": [
                        {
                            "aaaTacacsPlusProviderGroup": {
                                "attributes": {
                                    "dn": "uni/userext/tacacsext/tacacsplusprovidergroup-ISE"
                                },
                                "children": [
                                    {
                                        "aaaProviderRef": {
                                            "attributes": {
                                                "dn": "uni/userext/tacacsext/tacacsplusprovidergroup-ISE/providerref-198.18.1.72",
                                                "order": "2",
                                                "name": "198.18.1.72",
                                                "descr": "Added TACACS Server 198.18.1.72 - Brahma Startup Wizard"
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

resource "aci_rest" "auth-realm_console" {
	path		= "/api/node/mo/uni/userext/authrealm.json"
	class_name	= "aaaAuthRealm"
	payload		= <<EOF
{
    "aaaAuthRealm": {
        "attributes": {
            "dn": "uni/userext/authrealm"
        },
        "children": [
            {
                "aaaConsoleAuth": {
                    "attributes": {
                        "dn": "uni/userext/authrealm/consoleauth",
                        "realm": "tacacs",
                        "providerGroup": "ISE"
                    },
                    "children": []
                }
            }
        ]
    }
}
	EOF
}

resource "aci_rest" "auth-realm_default" {
	path		= "/api/node/mo/uni/userext/authrealm.json"
	class_name	= "aaaAuthRealm"
	payload		= <<EOF
{
    "aaaAuthRealm": {
        "attributes": {
            "dn": "uni/userext/authrealm"
        },
        "children": [
            {
                "aaaDefaultAuth": {
                    "attributes": {
                        "dn": "uni/userext/authrealm/defaultauth",
                        "realm": "local",
                        "providerGroup": ""
                    },
                    "children": []
                }
            }
        ]
    }
}
	EOF
}

