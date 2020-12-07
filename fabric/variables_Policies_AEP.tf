variable "policies_aep" {
	default = {
		"access" = {
			depends		= "aci_physical_domain.default[\"access\"]"
			description = "Base AEP Policy.  Used for Host/Device Connectivity to Fabric"
			name        = "access_aep"
			domain		= "uni/phys-access_phys"
		},
		"inband" = {
			depends		= "aci_physical_domain.default[\"Inband\"]"
			description = "Base AEP Policy.  Used for inband Device connectivity to Fabric"
			name        = "inband_aep"
			domain		= "uni/phys-inband_phys"
		},
		"l3out" = {
			depends		= "aci_l3_domain_profile.default[\"l3out\"]"
			description = "Base AEP Policy.  Used to Connect ACI Fabric to External Networks"
			name        = "l3out_aep"
			domain		= "uni/l3dom-l3out_L3"
		},
		"msite" = {
			depends		= "aci_l3_domain_profile.default[\"msite\"]"
			description = "Base AEP Policy.  Used to Connect ACI Fabrics to MultiSite Network"
			name        = "msite_aep"
			domain		= "uni/l3dom-msite_L3"
		},
	}
}