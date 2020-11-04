variable "lacp_policies" {
	default = {
		"Active" = {
			description = "Base LACP Policy; Mode Active"
			name        = "lacp.Active"
			mode        = "active"
		},
		"MacPin" = {
			description = "Base LACP Policy; Mode MAC Pinning"
			name        = "lacp.MacPin"
			mode        = "mac-pin"
		},
		"Passive" = {
			description = "Base LACP Policy; Mode Passive"
			name        = "lacp.Passive"
			mode        = "passive"
		},
		"Static" = {
			description = "Base LACP Policy; Mode Static"
			name        = "lacp.Static"
			mode        = "off"
		},
	}
}