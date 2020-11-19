variable "vlan_pool" {
	default = {
		"access_vl-pool" = {
			name        = "access_vl-pool"
			alloc_mode  = "static"
		},
		"dynamic_vl-pool" = {
			name        = "dynamic_vl-pool"
			alloc_mode  = "dynamic"
		},
		"inband_vl-pool" = {
			name        = "inband_vl-pool"
			alloc_mode  = "static"
		},
		"l3out_vl-pool" = {
			name        = "l3out_vl-pool"
			alloc_mode  = "static"
		},
		"msite_vl-pool" = {
			name        = "msite_vl-pool"
			alloc_mode  = "static"
		},
	}
}