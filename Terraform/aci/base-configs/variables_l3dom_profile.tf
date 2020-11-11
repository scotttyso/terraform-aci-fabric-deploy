variable "l3dom_profile" {
	default = {
		"Inband" = {
			name        = "inband_L3"
			vl_pool		= "inband_vl-pool"
		},
		"l3out" = {
			name        = "l3out_L3"
			vl_pool		= "l3out_vl-pool"
		},
		"msite" = {
			name        = "msite_L3"
			vl_pool		= "msite_vl-pool"
		},
	}
}