# This File will include VRFs

variable "user_vrfs" {
	default = {
		"prod_vrf" = {
			tenant_dn = ""
			name = "prod"
		},
	}
}