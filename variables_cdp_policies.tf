variable "cdp_policies" {
	default = {
		"Disabled" = {
			name        = "cdp.Disabled"
			admin_st    = "disabled"
		},
		"Enable" = {
			name        = "cdp.Enabled"
			admin_st    = "enabled"
		},
	}
}