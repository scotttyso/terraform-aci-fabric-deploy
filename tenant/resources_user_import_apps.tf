# This File will include Applications

resource "aci_application_profile" "prod_net_app" {
	depends_on = [aci_tenant.prod]
	tenant_dn  = aci_tenant.prod.id
	name       = "net_app"
}

resource "aci_application_profile" "dmz_net_app" {
	depends_on = [aci_tenant.dmz]
	tenant_dn  = aci_tenant.dmz.id
	name       = "net_app"
}

