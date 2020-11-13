variable "snmp_ctx_community" {
	default = {
		"mgmt_inb_cisco123" = {
			name        = "cisco123"
			tenant      = "mgmt"
			ctx         = "inb"
		},
		"mgmt_inb_read_access" = {
			name        = "read_access"
			tenant      = "mgmt"
			ctx         = "inb"
		},
		"mgmt_inb_redrum" = {
			name        = "redrum"
			tenant      = "mgmt"
			ctx         = "inb"
		},
		"mgmt_inb_will-this-work" = {
			name        = "will-this-work"
			tenant      = "mgmt"
			ctx         = "inb"
		},
		"mgmt_oob_cisco123" = {
			name        = "cisco123"
			tenant      = "mgmt"
			ctx         = "oob"
		},
		"mgmt_oob_read_access" = {
			name        = "read_access"
			tenant      = "mgmt"
			ctx         = "oob"
		},
		"mgmt_oob_redrum" = {
			name        = "redrum"
			tenant      = "mgmt"
			ctx         = "oob"
		},
		"mgmt_oob_will-this-work" = {
			name        = "will-this-work"
			tenant      = "mgmt"
			ctx         = "oob"
		},
	}
}
