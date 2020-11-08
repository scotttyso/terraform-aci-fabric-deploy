variable "interface_policies" {
	default = {
		"100M_Auto" = {
			name        = "100M_Auto"
			description = "Base Interface Policy; 100M Auto"
			auto_neg    = "on"
			speed       = "100M"
		},
		"100M_noNeg" = {
			name        = "100M_noNeg"
			description = "Base Interface Policy; 100M No negotiate"
			auto_neg    = "off"
			speed       = "100M"
		},
		"1G_Auto" = {
			name        = "1G_Auto"
			description = "Base Interface Policy; 1G Auto"
			auto_neg    = "on"
			speed       = "1G"
		},
		"1G_noNeg" = {
			name        = "1G_noNeg"
			description = "Base Interface Policy; 1G No negotiate"
			auto_neg    = "off"
			speed       = "1G"
		},
		"10G_Auto" = {
			name        = "10G_Auto"
			description = "Base Interface Policy; 10G Auto"
			auto_neg    = "on"
			speed       = "10G"
		},
		"10G_noNeg" = {
			name        = "10G_noNeg"
			description = "Base Interface Policy; 10G No negotiate"
			auto_neg    = "off"
			speed       = "10G"
		},
		"25G_Auto" = {
			name        = "25G_Auto"
			description = "Base Interface Policy; 25G Auto"
			auto_neg    = "on"
			speed       = "25G"
		},
		"25G_noNeg" = {
			name        = "25G_noNeg"
			description = "Base Interface Policy; 25G No negotiate"
			auto_neg    = "off"
			speed       = "25G"
		},
		"40G_Auto" = {
			name        = "40G_Auto"
			description = "Base Interface Policy; 40G Auto"
			auto_neg    = "on"
			speed       = "40G"
		},
		"40G_noNeg" = {
			name        = "40G_noNeg"
			description = "Base Interface Policy; 40G No negotiate"
			auto_neg    = "off"
			speed       = "40G"
		},
		"50G_Auto" = {
			name        = "50G_Auto"
			description = "Base Interface Policy; 50G Auto"
			auto_neg    = "on"
			speed       = "50G"
		},
		"50G_noNeg" = {
			name        = "50G_noNeg"
			description = "Base Interface Policy; 50G No negotiate"
			auto_neg    = "off"
			speed       = "50G"
		},
		"100G_Auto" = {
			name        = "100G_Auto"
			description = "Base Interface Policy; 100G Auto"
			auto_neg    = "on"
			speed       = "100G"
		},
		"100G_noNeg" = {
			name        = "100G_noNeg"
			description = "Base Interface Policy; 100G No negotiate"
			auto_neg    = "off"
			speed       = "100G"
		},
		"200G_Auto" = {
			name        = "200G_Auto"
			description = "Base Interface Policy; 200G Auto"
			auto_neg    = "on"
			speed       = "200G"
		},
		"200G_noNeg" = {
			name        = "200G_noNeg"
			description = "Base Interface Policy; 200G No negotiate"
			auto_neg    = "off"
			speed       = "200G"
		},
		"400G_Auto" = {
			name        = "400G_Auto"
			description = "Base Interface Policy; 400G Auto"
			auto_neg    = "on"
			speed       = "400G"
		},
		"400G_noNeg" = {
			name        = "400G_noNeg"
			description = "Base Interface Policy; 400G No negotiate"
			auto_neg    = "off"
			speed       = "400G"
		},
		"inherit_Auto" = {
			name        = "inherit_Auto"
			description = "Base Interface Policy; Inherit Auto"
			auto_neg    = "on"
			speed       = "inherit"
		},
		"inherit_noNeg" = {
			name        = "inherit_noNeg"
			description = "Base Interface Policy; Inherit No negotiate"
			auto_neg    = "off"
			speed       = "inherit"
		},
	}
}