resource "aci_tenant" "default" {
	for_each    = var.default_tenants
	name        = each.value.name
	description = each.value.description
}

resource "aci_tenant" "user_tenants" {
	for_each    = var.user_tenants
	name        = each.value.name
	description = each.value.description
}