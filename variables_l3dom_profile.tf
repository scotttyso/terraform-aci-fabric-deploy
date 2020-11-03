variable "l3dom_profile" {
	default = {
		"Inband" = {
			name        = "inband.L3"
		},
		"l3out" = {
			name        = "l3out.L3"
		},
		"msite" = {
			name        = "msite.L3"
		},
	}
}