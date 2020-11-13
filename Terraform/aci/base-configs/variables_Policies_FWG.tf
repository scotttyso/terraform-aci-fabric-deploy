variable "policies_fwg" {
	default = {
		"fwg_A" = {
			name        = "fwg_A"
			firmware_group_type = "range"
		},
		"fwg_B" = {
			name        = "fwg_B"
			firmware_group_type = "range"
		},
	}
}