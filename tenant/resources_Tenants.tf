resource "aci_tenant" "default" {
	for_each    = var.default_tenants
	name        = each.value.name
	description = each.value.description
}