# This File will include Tenants

resource "aci_tenant" "prod" {
	description    = "Example Prod Tenant"
	name           = "prod"
}

resource "aci_tenant" "dmz" {
	description    = "Example DMZ Tenant"
	name           = "dmz"
}

