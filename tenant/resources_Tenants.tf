resource "aci_tenant" "default" {
	for_each    = var.default_tenants
	description = each.value.description
	name        = each.value.name
}

data "aci_contract" "default" {
	tenant_dn	= "uni/tn-common"
	name		= "default"
}