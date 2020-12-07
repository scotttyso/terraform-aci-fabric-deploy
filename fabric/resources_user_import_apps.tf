# This File will include Applications

resource "aci_application_profile" "dmz_nets" {
	depends_on = [aci_tenant.dmz]
	tenant_dn  = aci_tenant.dmz.id
	name       = "nets"
	prio       = "unspecified"
}

resource "aci_application_profile" "prod_nets" {
	depends_on = [aci_tenant.prod]
	tenant_dn  = aci_tenant.prod.id
	name       = "nets"
	prio       = "unspecified"
}

resource "aci_application_profile" "prod_sap_app" {
	depends_on = [aci_tenant.prod]
	tenant_dn  = aci_tenant.prod.id
	name       = "sap_app"
	prio       = "level3"
}

resource "aci_application_profile" "prod_sap_db" {
	depends_on = [aci_tenant.prod]
	tenant_dn  = aci_tenant.prod.id
	name       = "sap_db"
	prio       = "level3"
}

resource "aci_application_profile" "prod_sap_intg" {
	depends_on = [aci_tenant.prod]
	tenant_dn  = aci_tenant.prod.id
	name       = "sap_intg"
	prio       = "level3"
}

