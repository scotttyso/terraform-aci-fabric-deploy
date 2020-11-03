resource "aci_leaf_profile" "example" {
  for_each    = var.leaf_profile
  name        = each.value.name
  leaf_selector {
    name        = each.value.name
    switch_association_type = "range"
    node_block {
      name  	= each.value.name
      from_ 	= each.value.node_id
      to_   	= each.value.node_id
    }
  }
}

resource "aci_leaf_interface_profile" "example" {
	for_each    = var.leaf_profile
	name        = each.value.name
}

resource "aci_rest" "leaf_int_selector" {
	for_each	= var.leaf_profile
	path		= "/api/node/mo/uni/infra/nprof-${each.value.name}.json"
	payload		= <<EOF
{
	"infraRsAccPortP": {
		"attributes": {
			"tDn": "uni/infra/accportprof-${each.value.name}"
		}
	}
}
	EOF
}

resource "aci_access_port_selector" "Leaf101" {
	for_each					= var.port_selector_48
	leaf_interface_profile_dn 	= aci_leaf_interface_profile.example["Leaf101"].id
	name                      	= each.value.name
	access_port_selector_type 	= "range"
}

resource "aci_access_port_selector" "Leaf102" {
	for_each					= var.port_selector_48
	leaf_interface_profile_dn 	= aci_leaf_interface_profile.example["Leaf102"].id
	name                      	= each.value.name
	access_port_selector_type 	= "range"
}
