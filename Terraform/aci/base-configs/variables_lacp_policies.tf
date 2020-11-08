variable "lacp_policies" {
	default = {
		"Active" = {
			description = "Base LACP Policy; Mode Active"
			name        = "lacp_Active"
			mode        = "active"
		},
		"MacPin" = {
			description = "Base LACP Policy; Mode MAC Pinning"
			name        = "lacp_MacPin"
			mode        = "mac-pin"
		},
		"Passive" = {
			description = "Base LACP Policy; Mode Passive"
			name        = "lacp_Passive"
			mode        = "passive"
		},
		"Static" = {
			description = "Base LACP Policy; Mode Static"
			name        = "lacp_Static"
			mode        = "off"
		},
	}
}