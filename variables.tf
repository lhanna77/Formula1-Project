# general

variable "location" { default = "US" }
variable "project" { default = "mstr-globalbi-sbx-c730" }
variable "region" { default = "us-east1" }
variable "env" { default = "sbx" }
variable "schema_folder_path" { default = "files/silver/table_schemas" }

variable "stage" { 
    type = map
    default = {
        "raw" = "bronze"
        "processed" = "silver"
        "presentation" = "gold"
    } 
}

locals {
  local_zone = "${var.region}-b"
}