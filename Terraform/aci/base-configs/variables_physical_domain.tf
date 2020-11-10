variable "physical_domain" {
	default = {
		"access" = {
			name        = "access_phys"
			vl-pool     = "access_vl-pool"
		},
		"Inband" = {
			name        = "inband_phys"
			vl-pool		= "inband_vl-pool"
		},
	}
}