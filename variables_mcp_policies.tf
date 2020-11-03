variable "mcp_policies" {
	default = {
		"mcp.Disabled" = {
			description = "Base Miscabling Policy; Mode Disabled"
			name        = "mcp.Disabled"
			admin_st    = "disabled"
		},
		"mcp.Enabled" = {
			description = "Base LACP Policy; Mode Enabled"
			name        = "mcp.Enabled"
			admin_st    = "enabled"
		},
	}
}