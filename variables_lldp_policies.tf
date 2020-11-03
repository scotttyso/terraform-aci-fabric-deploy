variable "lldp_policies" {
	default = {
		"Disabled" = {
			description = "Base LLDP Policy; Disabled"
			name        = "lldp.Disabled"
			admin_rx_st = "disabled"
			admin_tx_st = "disabled"
		},
		"Enabled" = {
			description = "Base LLDP Policy; Enabled"
			name        = "lldp.Enabled"
			admin_rx_st = "enabled"
			admin_tx_st = "enabled"
		},
	}
}