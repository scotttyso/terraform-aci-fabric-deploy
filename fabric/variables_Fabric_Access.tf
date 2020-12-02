variable "breakouts" {
	default = {
		"2x100g_pg" = {
			description = "400G to 2x100g"
			name        = "2x100g_pg"
			map			= "100g-2x"
		},
		"4x10g_pg" = {
			description = "40G to 4x10g"
			name        = "4x10g_pg"
			map			= "10g-4x"
		},
		"4x25g_pg" = {
			description = "100G to 4x25g"
			name        = "4x25g_pg"
			map			= "25g-4x"
		},
		"4x100g_pg" = {
			description = "400G to 4x100g"
			name        = "4x100g_pg"
			map			= "100g-4x"
		},
		"8x50g_pg" = {
			description = "400G to 8x50g"
			name        = "8x50g_pg"
			map			= "50g-8x"
		},
	}
}