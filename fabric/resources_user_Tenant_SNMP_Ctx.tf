resource "aci_rest" "snmp_ctx" {
	for_each        = var.snmp_ctx
	path            = "/api/node/mo/uni/tn-${each.value.tenant}/ctx-${each.value.ctx}/snmpctx.json"
	class_name      = "vzOOBBrCP"
	payload         = <<EOF
{
    "snmpCtxP": {
        "attributes": {
            "dn": "uni/tn-${each.value.tenant}/ctx-${each.value.ctx}/snmpctx",
            "name": "${each.value.name}",
            "rn": "snmpctx"
        },
        "children": []
    }
}
	EOF
}

resource "aci_rest" "snmp_ctx_community" {
	for_each        = var.snmp_ctx_community
	depends_on      = [aci_tenant.mgmt]
	path            = "/api/node/mo/uni/tn-${each.value.tenant}/ctx-${each.value.ctx}/snmpctx/community-${each.value.name}.json"
	class_name      = "vzOOBBrCP"
	payload         = <<EOF
{
    "snmpCommunityP": {
        "attributes": {
            "dn": "uni/tn-${each.value.tenant}/ctx-${each.value.ctx}/snmpctx/community-${each.value.name}",
            "name": "${each.value.name}",
            "descr": "Adding Community ${each.value.name} to Ctx",
            "rn": "community-${each.value.name}"
        },
        "children": []
    }
}
	EOF
}
