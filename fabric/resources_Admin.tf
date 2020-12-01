resource "aci_pod_maintenance_group" "default" {
	for_each    = var.admin_maintgroup
    name  = each.value.name
    fwtype  = each.value.fwtype
}

resource "aci_firmware_group" "default" {
	for_each   			= var.admin_fwg
	name       			= each.value.name
	firmware_group_type = each.value.firmware_group_type
}
