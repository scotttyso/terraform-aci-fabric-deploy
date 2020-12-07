resource "aci_epg_to_static_path" "dmz_nets_v0995_epg_202_Eth1-03" {
	depends_on           = [aci_application_epg.dmz_nets_v0995_epg,aci_ranges.st_vlan_pool_add_995]
	application_epg_dn   = aci_application_epg.dmz_nets_v0995_epg.id
	tdn                  = "topology/pod-1/paths-202/pathep-[eth1/03]"
	encap                = "vlan-995"
	mode                 = "native"
}

resource "aci_epg_to_static_path" "dmz_nets_v0995_epg_202_Eth1-04" {
	depends_on           = [aci_application_epg.dmz_nets_v0995_epg,aci_ranges.st_vlan_pool_add_995]
	application_epg_dn   = aci_application_epg.dmz_nets_v0995_epg.id
	tdn                  = "topology/pod-1/paths-202/pathep-[eth1/04]"
	encap                = "vlan-995"
	mode                 = "native"
}

resource "aci_epg_to_static_path" "prod_nets_v0691_epg_202_Eth1-07" {
	depends_on           = [aci_application_epg.prod_nets_v0691_epg,aci_ranges.st_vlan_pool_add_691]
	application_epg_dn   = aci_application_epg.prod_nets_v0691_epg.id
	tdn                  = "topology/pod-1/paths-202/pathep-[eth1/07]"
	encap                = "vlan-691"
	mode                 = "native"
}

