# This File will include Bridge Domains

resource "aci_bridge_domain" "v0056_bd" {
	depends_on                  = [aci_vrf.dmz_vrf]
	tenant_dn                   = aci_tenant.dmz.id
	description                 = "Network Centric"
	name                        = "v0056_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.dmz_vrf.id
}

resource "aci_bridge_domain" "v0995_bd" {
	depends_on                  = [aci_vrf.dmz_vrf]
	tenant_dn                   = aci_tenant.dmz.id
	description                 = "Network Centric"
	name                        = "v0995_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.dmz_vrf.id
}

resource "aci_bridge_domain" "v0996_bd" {
	depends_on                  = [aci_vrf.dmz_vrf]
	tenant_dn                   = aci_tenant.dmz.id
	description                 = "Network Centric"
	name                        = "v0996_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.dmz_vrf.id
}

resource "aci_bridge_domain" "v0999_bd" {
	depends_on                  = [aci_vrf.dmz_vrf]
	tenant_dn                   = aci_tenant.dmz.id
	description                 = "Network Centric"
	name                        = "v0999_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.dmz_vrf.id
}

resource "aci_bridge_domain" "v0001_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v0001_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v0064_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v0064_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v0080_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v0080_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v0087_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v0087_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v0090_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v0090_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v0091_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v0091_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v0110_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v0110_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v0136_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v0136_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v0168_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v0168_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v0169_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v0169_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v0691_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v0691_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v0811_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v0811_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v0812_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v0812_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v0997_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v0997_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v0998_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v0998_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v3001_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v3001_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v3003_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v3003_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v3004_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v3004_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v3006_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v3006_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v3007_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v3007_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v3011_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v3011_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v3019_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v3019_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v3103_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v3103_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v3910_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v3910_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v3960_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v3960_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v3961_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v3961_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v3962_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v3962_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v3963_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v3963_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v3964_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v3964_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v3965_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v3965_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v3966_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v3966_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "v3967_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "Network Centric"
	name                        = "v3967_bd"
	optimize_wan_bandwidth      = "no"
	arp_flood                   = "yes"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "flood"
	unk_mcast_act               = "flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "sap_app_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "None"
	name                        = "sap_app_bd"
	optimize_wan_bandwidth      = "yes"
	arp_flood                   = "no"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "proxy"
	unk_mcast_act               = "opt-flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "sap_db_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "None"
	name                        = "sap_db_bd"
	optimize_wan_bandwidth      = "yes"
	arp_flood                   = "no"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "proxy"
	unk_mcast_act               = "opt-flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

resource "aci_bridge_domain" "sap_itg_bd" {
	depends_on                  = [aci_vrf.prod_vrf]
	tenant_dn                   = aci_tenant.prod.id
	description                 = "None"
	name                        = "sap_itg_bd"
	optimize_wan_bandwidth      = "yes"
	arp_flood                   = "no"
	ep_move_detect_mode         = "garp"
	ip_learning                 = "yes"
	ipv6_mcast_allow            = "no"
	limit_ip_learn_to_subnets   = "yes"
	mcast_allow                 = "yes"
	multi_dst_pkt_act           = "bd-flood"
	bridge_domain_type          = "regular"
	unk_mac_ucast_act           = "proxy"
	unk_mcast_act               = "opt-flood"
	relation_fv_rs_ctx          = aci_vrf.prod_vrf.id
}

