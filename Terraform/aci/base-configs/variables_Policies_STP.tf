variable "policies_stp" {
	default = {
		"BPDU_ft" = {
			name        = "BPDU_ft"
			ctrl		= "bpdu-filter"
		},
		"BPDU_fg" = {
			name        = "BPDU_fg"
			ctrl		= "bpdu-filter,bpdu-guard"
		},
		"BPDU_gd" = {
			name        = "BPDU_gd"
			ctrl		= "bpdu-guard"
		},
	}
}