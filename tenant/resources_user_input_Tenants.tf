# This File will include Tenants

resource "aci_tenant" "prod" {
	name        = "prod"
	description = "Example Prod Tenant"
}

resource "aci_tenant" "dmz" {
	name        = "dmz"
	description = "Example DMZ Tenant"
}

