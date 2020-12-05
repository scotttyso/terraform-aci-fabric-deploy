variable "default_tenants" {
	default = {
		"common" = {
			description = "This is the common Tenant.  System Default"
			name        = "common"
		},
		"infra" = {
			description = "This is the infra Tenant.  System Default"
			name        = "infra"
		},
		"mgmt" = {
			description = "This is the mgmt Tenant.  System Default"
			name        = "mgmt"
		},
	}
}