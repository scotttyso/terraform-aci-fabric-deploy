variable "vlan_pool" {
	default = {
		"dynamic_vl-pool" = {
			name        = "dynamic_vl-pool"
			alloc_mode  = "dynamic"
		},
		"inband_vl-pool" = {
			name        = "inband_vl-pool"
			alloc_mode  = "static"
		},
		"msite_vl-pool" = {
			name        = "msite_vl-pool"
			alloc_mode  = "static"
		},
		"static_vl-pool" = {
			name        = "static_vl-pool"
			alloc_mode  = "static"
		},
	}
}