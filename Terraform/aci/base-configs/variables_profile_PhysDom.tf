variable "profile_physdom" {
	default = {
		"access" = {
			name        = "access_phys"
			vl_pool		= "access_vl-pool"
		},
		"Inband" = {
			name        = "inband_phys"
			vl_pool		= "inband_vl-pool"
		},
	}
}