variable "l3dom_profile" {
	default = {
		"Inband" = {
			name        = "inband_L3"
		},
		"l3out" = {
			name        = "l3out_L3"
		},
		"msite" = {
			name        = "msite_L3"
		},
	}
}