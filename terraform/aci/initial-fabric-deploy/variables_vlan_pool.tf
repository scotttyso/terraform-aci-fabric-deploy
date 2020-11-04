variable "vlan_pool" {
	default = {
		"dynamic.vl-pool" = {
			name        = "dynamic.vl-pool"
			alloc_mode  = "dynamic"
		},
		"inband.vl-pool" = {
			name        = "inband.vl-pool"
			alloc_mode  = "static"
		},
		"msite.vl-pool" = {
			name        = "msite.vl-pool"
			alloc_mode  = "static"
		},
		"static.vl-pool" = {
			name        = "static.vl-pool"
			alloc_mode  = "static"
		},
	}
}