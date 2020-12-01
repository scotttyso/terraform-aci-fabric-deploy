# This File will include Tenants

variable "user_tenants" {
	default = {
		"prod" = {
			description = "Example Prod Tenant"
			name = "prod"
		},
		"dmz" = {
			description = "Example DMZ Tenant"
			name = "dmz"
		},
	}
}