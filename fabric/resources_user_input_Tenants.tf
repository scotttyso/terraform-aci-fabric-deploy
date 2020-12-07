# This File will include Tenants

data "aci_tenant" "common" {	name    = "common"}

data "aci_tenant" "infra" {	name    = "infra"}

data "aci_tenant" "mgmt" {	name    = "mgmt"}

resource "aci_tenant" "prod" {
	description    = "Example Prod Tenant"
	name           = "prod"
}

resource "aci_tenant" "dmz" {
	description    = "Example DMZ Tenant"
	name           = "dmz"
}

