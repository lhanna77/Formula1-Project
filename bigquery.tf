locals {
    silver_dataset = element(values(var.stage), 1)
    file_names_ext = [for file in fileset(var.schema_folder_path,"*") : file]
}

resource "google_bigquery_dataset" "f1_dataset" {
    for_each = var.stage
    project = var.project
    dataset_id = "lh_f1_${each.value}"
    description = "lh formula1 training dataset"
    location = var.location
    
}

resource "google_bigquery_table" "f1_tables" {
  count = length(local.file_names_ext)
  deletion_protection=false
  project = var.project
  dataset_id = "lh_f1_${local.silver_dataset}" #var.dataset_id
  table_id = trimsuffix("${local.file_names_ext[count.index]}", ".json")
  description = ""
   time_partitioning {
      type = "DAY"
      field = "ingestion_date"
    }
  schema = file("/${var.schema_folder_path}/${local.file_names_ext[count.index]}")
  

  depends_on = [ google_bigquery_dataset.f1_dataset ]

} 

output "dataset_id" { value = {for key, dataset in google_bigquery_dataset.f1_dataset : key => dataset.dataset_id} }
output "file_names_ext" { value = local.file_names_ext }
output "silver_dataset" { value = local.silver_dataset }
