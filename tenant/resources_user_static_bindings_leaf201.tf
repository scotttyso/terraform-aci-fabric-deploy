resource "aci_epg_to_static_path" "leaf201_Eth1-1-03_v0995_epg" {
	depends_on           = [aci_application_epg.v0995_epg,aci_range.st_vlan_pool_995]
	application_epg_dn   = aci_application_epg.v0995_epg.id
	tdn                  = "topology/pod-1/paths-201/pathep-[eth1/1/3]"
	encap                = "vlan-995"
	mode                 = "native"
}

resource "aci_epg_to_static_path" "leaf201_Eth1-1-04_v0995_epg" {
	depends_on           = [aci_application_epg.v0995_epg,aci_range.st_vlan_pool_995]
	application_epg_dn   = aci_application_epg.v0995_epg.id
	tdn                  = "topology/pod-1/paths-201/pathep-[eth1/1/4]"
	encap                = "vlan-995"
	mode                 = "native"
}

resource "aci_epg_to_static_path" "leaf201_Eth1-04_v0691_epg" {
	depends_on           = [aci_application_epg.v0691_epg,aci_range.st_vlan_pool_691]
	application_epg_dn   = aci_application_epg.v0691_epg.id
	tdn                  = "topology/pod-1/paths-201/pathep-[eth1/4]"
	encap                = "vlan-691"
	mode                 = "native"
}

