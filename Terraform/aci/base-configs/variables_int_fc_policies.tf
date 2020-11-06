variable "int_fc_policies" {
	default = {
		"4G.f_port" = {
			name        = "4G.f_port"
			port_mode	= "f"
			speed       = "4G"
			trunk_mode  = "auto"
		},
		"4G.f_trunk" = {
			name        = "4G.f_trunk"
			port_mode	= "f"
			speed       = "4G"
			trunk_mode  = "trunk-on"
		},
		"4G.np_port" = {
			name        = "4G.np_port"
			port_mode	= "np"
			speed       = "4G"
			trunk_mode  = "auto"
		},
		"4G.np_trunk" = {
			name        = "4G.np_trunk"
			port_mode	= "np"
			speed       = "4G"
			trunk_mode  = "trunk-on"
		},
		"8G.f_port" = {
			name        = "8G.f_port"
			port_mode	= "f"
			speed       = "8G"
			trunk_mode  = "auto"
		},
		"8G.f_trunk" = {
			name        = "8G.f_trunk"
			port_mode	= "f"
			speed       = "8G"
			trunk_mode  = "trunk-on"
		},
		"8G.np_port" = {
			name        = "8G.np_port"
			port_mode	= "np"
			speed       = "8G"
			trunk_mode  = "auto"
		},
		"8G.np_trunk" = {
			name        = "8G.np_trunk"
			port_mode	= "np"
			speed       = "8G"
			trunk_mode  = "trunk-on"
		},
		"16G.f_port" = {
			name        = "16G.f_port"
			port_mode	= "f"
			speed       = "16G"
			trunk_mode  = "auto"
		},
		"16G.f_trunk" = {
			name        = "16G.f_trunk"
			port_mode	= "f"
			speed       = "16G"
			trunk_mode  = "trunk-on"
		},
		"16G.np_port" = {
			name        = "16G.np_port"
			port_mode	= "np"
			speed       = "16G"
			trunk_mode  = "auto"
		},
		"16G.np_trunk" = {
			name        = "16G.np_trunk"
			port_mode	= "np"
			speed       = "16G"
			trunk_mode  = "trunk-on"
		},
		"32G.f_port" = {
			name        = "32G.f_port"
			port_mode	= "f"
			speed       = "32G"
			trunk_mode  = "auto"
		},
		"32G.f_trunk" = {
			name        = "32G.f_trunk"
			port_mode	= "f"
			speed       = "32G"
			trunk_mode  = "trunk-on"
		},
		"32G.np_port" = {
			name        = "32G.np_port"
			port_mode	= "np"
			speed       = "32G"
			trunk_mode  = "auto"
		},
		"32G.np_trunk" = {
			name        = "32G.np_trunk"
			port_mode	= "np"
			speed       = "32G"
			trunk_mode  = "trunk-on"
		},
	}
}