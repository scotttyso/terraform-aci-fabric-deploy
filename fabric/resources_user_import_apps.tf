# This File will include Applications

resource "aci_application_profile" "prod_nets" {
	depends_on = [aci_tenant.prod]
	tenant_dn  = aci_tenant.prod.id
	name       = "nets"
}

resource "aci_application_profile" "dmz_nets" {
	depends_on = [aci_tenant.dmz]
	tenant_dn  = aci_tenant.dmz.id
	name       = "nets"
}

