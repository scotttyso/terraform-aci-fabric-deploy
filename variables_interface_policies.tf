variable "interface_policies" {
	default = {
		"100M.Auto" = {
			name        = "100M.Auto"
			description = "Base Interface Policy; 100M Auto"
			auto_neg    = "on"
			speed       = "100M"
		},
		"100M.noNeg" = {
			name        = "100M.noNeg"
			description = "Base Interface Policy; 100M No negotiate"
			auto_neg    = "off"
			speed       = "100M"
		},
		"1G.Auto" = {
			name        = "1G.Auto"
			description = "Base Interface Policy; 1G Auto"
			auto_neg    = "on"
			speed       = "1G"
		},
		"1G.noNeg" = {
			name        = "1G.noNeg"
			description = "Base Interface Policy; 1G No negotiate"
			auto_neg    = "off"
			speed       = "1G"
		},
		"10G.Auto" = {
			name        = "10G.Auto"
			description = "Base Interface Policy; 10G Auto"
			auto_neg    = "on"
			speed       = "10G"
		},
		"10G.noNeg" = {
			name        = "10G.noNeg"
			description = "Base Interface Policy; 10G No negotiate"
			auto_neg    = "off"
			speed       = "10G"
		},
		"25G.Auto" = {
			name        = "25G.Auto"
			description = "Base Interface Policy; 25G Auto"
			auto_neg    = "on"
			speed       = "25G"
		},
		"25G.noNeg" = {
			name        = "25G.noNeg"
			description = "Base Interface Policy; 25G No negotiate"
			auto_neg    = "off"
			speed       = "25G"
		},
		"40G.Auto" = {
			name        = "40G.Auto"
			description = "Base Interface Policy; 40G Auto"
			auto_neg    = "on"
			speed       = "40G"
		},
		"40G.noNeg" = {
			name        = "40G.noNeg"
			description = "Base Interface Policy; 40G No negotiate"
			auto_neg    = "off"
			speed       = "40G"
		},
		"50G.Auto" = {
			name        = "50G.Auto"
			description = "Base Interface Policy; 50G Auto"
			auto_neg    = "on"
			speed       = "50G"
		},
		"50G.noNeg" = {
			name        = "50G.noNeg"
			description = "Base Interface Policy; 50G No negotiate"
			auto_neg    = "off"
			speed       = "50G"
		},
		"100G.Auto" = {
			name        = "100G.Auto"
			description = "Base Interface Policy; 100G Auto"
			auto_neg    = "on"
			speed       = "100G"
		},
		"100G.noNeg" = {
			name        = "100G.noNeg"
			description = "Base Interface Policy; 100G No negotiate"
			auto_neg    = "off"
			speed       = "100G"
		},
		"200G.Auto" = {
			name        = "200G.Auto"
			description = "Base Interface Policy; 200G Auto"
			auto_neg    = "on"
			speed       = "200G"
		},
		"200G.noNeg" = {
			name        = "200G.noNeg"
			description = "Base Interface Policy; 200G No negotiate"
			auto_neg    = "off"
			speed       = "200G"
		},
		"400G.Auto" = {
			name        = "400G.Auto"
			description = "Base Interface Policy; 400G Auto"
			auto_neg    = "on"
			speed       = "400G"
		},
		"400G.noNeg" = {
			name        = "400G.noNeg"
			description = "Base Interface Policy; 400G No negotiate"
			auto_neg    = "off"
			speed       = "400G"
		},
	}
}