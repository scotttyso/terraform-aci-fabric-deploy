variable "policies_int_fc" {
	default = {
		"4G_f_port" = {
			name        = "4G_f_port"
			port_mode	= "f"
			speed       = "4G"
			trunk_mode  = "auto"
		},
		"4G_f_trunk" = {
			name        = "4G_f_trunk"
			port_mode	= "f"
			speed       = "4G"
			trunk_mode  = "trunk-on"
		},
		"4G_np_port" = {
			name        = "4G_np_port"
			port_mode	= "np"
			speed       = "4G"
			trunk_mode  = "auto"
		},
		"4G_np_trunk" = {
			name        = "4G_np_trunk"
			port_mode	= "np"
			speed       = "4G"
			trunk_mode  = "trunk-on"
		},
		"8G_f_port" = {
			name        = "8G_f_port"
			port_mode	= "f"
			speed       = "8G"
			trunk_mode  = "auto"
		},
		"8G_f_trunk" = {
			name        = "8G_f_trunk"
			port_mode	= "f"
			speed       = "8G"
			trunk_mode  = "trunk-on"
		},
		"8G_np_port" = {
			name        = "8G_np_port"
			port_mode	= "np"
			speed       = "8G"
			trunk_mode  = "auto"
		},
		"8G_np_trunk" = {
			name        = "8G_np_trunk"
			port_mode	= "np"
			speed       = "8G"
			trunk_mode  = "trunk-on"
		},
		"16G_f_port" = {
			name        = "16G_f_port"
			port_mode	= "f"
			speed       = "16G"
			trunk_mode  = "auto"
		},
		"16G_f_trunk" = {
			name        = "16G_f_trunk"
			port_mode	= "f"
			speed       = "16G"
			trunk_mode  = "trunk-on"
		},
		"16G_np_port" = {
			name        = "16G_np_port"
			port_mode	= "np"
			speed       = "16G"
			trunk_mode  = "auto"
		},
		"16G_np_trunk" = {
			name        = "16G_np_trunk"
			port_mode	= "np"
			speed       = "16G"
			trunk_mode  = "trunk-on"
		},
		"32G_f_port" = {
			name        = "32G_f_port"
			port_mode	= "f"
			speed       = "32G"
			trunk_mode  = "auto"
		},
		"32G_f_trunk" = {
			name        = "32G_f_trunk"
			port_mode	= "f"
			speed       = "32G"
			trunk_mode  = "trunk-on"
		},
		"32G_np_port" = {
			name        = "32G_np_port"
			port_mode	= "np"
			speed       = "32G"
			trunk_mode  = "auto"
		},
		"32G_np_trunk" = {
			name        = "32G_np_trunk"
			port_mode	= "np"
			speed       = "32G"
			trunk_mode  = "trunk-on"
		},
	}
}