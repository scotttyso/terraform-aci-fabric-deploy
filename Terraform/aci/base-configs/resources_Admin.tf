resource "aci_pod_maintenance_group" "default" {
	for_each    = var.admin_maintgroup
    name  = each.value.name
    fwtype  = each.value.fwtype
}