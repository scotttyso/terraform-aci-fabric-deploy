  
provider "aci" {
	username    = var.aciUser
	password    = var.aciPass
	url         = var.aciUrl
	insecure    = true
}