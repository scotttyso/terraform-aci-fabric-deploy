variable "policies_mcp" {
	default = {
		"mcp_Disabled" = {
			description = "Base Miscabling Policy; Mode Disabled"
			name        = "mcp_Disabled"
			admin_st    = "disabled"
		},
		"mcp_Enabled" = {
			description = "Base LACP Policy; Mode Enabled"
			name        = "mcp_Enabled"
			admin_st    = "enabled"
		},
	}
}