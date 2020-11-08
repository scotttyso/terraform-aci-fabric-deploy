variable "aep_policies" {
	default = {
		"access" = {
			description = "Base AEP Policy.  Used for Host/Device Connectivity to Fabric"
			name        = "access_aep"
		},
		"inband" = {
			description = "Base AEP Policy.  Used for inband Device connectivity to Fabric"
			name        = "inband_aep"
		},
		"l3out" = {
			description = "Base AEP Policy.  Used to Connect ACI Fabric to External Networks"
			name        = "l3out_aep"
		},
		"msite" = {
			description = "Base AEP Policy.  Used to Connect ACI Fabrics to MultiSite Network"
			name        = "msite_aep"
		},
	}
}