terraform {
  required_version = "> 0.13"
  required_providers {
    aci = {
      source = "ciscodevnet/aci"
      version = "= 0.5.2"
    }
  }
}
