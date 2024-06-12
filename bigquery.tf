locals {
    silver_dataset = element(values(var.stage), 1)
    file_names_silver = [for file in fileset(var.schema_folder_path_silver,"*") : file]

    gold_dataset = element(values(var.stage), 0)
    file_names_gold = [for file in fileset(var.schema_folder_path_gold,"*") : file]

}

resource "google_bigquery_dataset" "f1_dataset" {
    for_each = var.stage
    project = var.project
    dataset_id = "lh_f1_${each.value}"
    description = "lh formula1 training dataset"
    location = var.location
    
}

resource "google_bigquery_table" "f1_silver_tables" {
  count = length(local.file_names_silver)
  deletion_protection=false
  project = var.project
  dataset_id = "lh_f1_${local.silver_dataset}"
  table_id = trimsuffix("${local.file_names_silver[count.index]}", ".json")
  description = ""
   time_partitioning {
      type = "DAY"
      field = "ingestion_date"
    }
  schema = file("/${var.schema_folder_path_silver}/${local.file_names_silver[count.index]}")
  

  depends_on = [ google_bigquery_dataset.f1_dataset ]

} 

resource "google_bigquery_table" "f1_gold_tables" {
  count = length(local.file_names_gold)
  deletion_protection=false
  project = var.project
  dataset_id = "lh_f1_${local.gold_dataset}"
  table_id = trimsuffix("${local.file_names_gold[count.index]}", ".json")
  description = ""
  #  time_partitioning {
  #     type = "DAY"
  #     field = "ingestion_date"
  #   }
  schema = file("/${var.schema_folder_path_gold}/${local.file_names_gold[count.index]}")
  

  depends_on = [ google_bigquery_dataset.f1_dataset ]

} 

output "dataset_id" { value = {for key, dataset in google_bigquery_dataset.f1_dataset : key => dataset.dataset_id} }
output "silver_dataset" { value = local.silver_dataset }
output "file_names_silver" { value = local.file_names_silver }
output "gold_dataset" { value = local.gold_dataset }
output "file_names_gold" { value = local.file_names_gold }


