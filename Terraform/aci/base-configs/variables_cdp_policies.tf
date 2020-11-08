variable "cdp_policies" {
	default = {
		"Disabled" = {
			name        = "cdp_Disabled"
			admin_st    = "disabled"
		},
		"Enable" = {
			name        = "cdp_Enabled"
			admin_st    = "enabled"
		},
	}
}