# general

variable "location" { default = "US" }
variable "project" { default = "mstr-globalbi-sbx-c730" }
variable "region" { default = "us-east1" }
variable "env" { default = "sbx" }

variable "schema_folder_path_silver" { default = "files/latest_data_from_api/silver/table_schemas" }
variable "schema_folder_path_gold" { default = "files/latest_data_from_api/gold/report_schemas" }

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