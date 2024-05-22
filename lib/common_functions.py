# Databricks notebook source

from datetime import date
from pyspark.sql import SparkSession
from pandas import ExcelWriter
from pathlib import Path
from os import path
from requests import request
from csv import reader as csv_reader, writer as csv_writer

def get_ingestion_date():
  #date_today = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
  date_today = date.today().strftime("%Y-%m-%d")
  
  return date_today

def get_spark_session():
  spark = SparkSession.builder.appName('formula1').getOrCreate()
  
  return spark

def get_relpath(file_location):
	
	ROOT_DIR = Path(__file__).parents[2]
	rel_file_path = Path(path.join(ROOT_DIR, file_location))
	
	return rel_file_path

def add_to_excel(file_path, df, sheet_name):
    output_dir = get_relpath(file_path)

    with ExcelWriter(output_dir) as writer:
        df.to_excel(writer, sheet_name=sheet_name)
        
    print(f'\n{df} added to  - {output_dir}.\n')

def add_header_to_excel(target_file,header_text):
    with open(target_file,'w',encoding='utf-8',newline='') as file:
      file.write(header_text)
      file.write("\n")

def call_api(url):
  
  json_url = url + '.json?limit=1000'
  response = request("GET", json_url)

  return response.json()

def re_arrange_partition_column(input_df, partition_column):
  column_list = []
  for column_name in input_df.schema.names:
    if column_name != partition_column:
      column_list.append(column_name)
  column_list.append(partition_column)
  output_df = input_df.select(column_list)
  
  return output_df


def overwrite_partition(input_df, db_name, table_name, partition_column):
  output_df = re_arrange_partition_column(input_df, partition_column)
  spark.conf.set("spark.sql.sources.partitionOverwriteMode","dynamic")
  if (spark._jsparkSession.catalog().tableExists(f"{db_name}.{table_name}")):
    output_df.write.mode("overwrite").insertInto(f"{db_name}.{table_name}")
  else:
    output_df.write.mode("overwrite").partitionBy(partition_column).format("parquet").saveAsTable(f"{db_name}.{table_name}")

def df_column_to_list(input_df, column_name):
  df_row_list = input_df.select(column_name) \
                        .distinct() \
                        .collect()
  
  column_value_list = [row[column_name] for row in df_row_list]
  
  return column_value_list

def merge_delta_data(input_df, db_name, table_name, folder_path, merge_condition, partition_column):
  spark.conf.set("spark.databricks.optimizer.dynamicPartitionPruning","true")

  from delta.tables import DeltaTable
  if (spark._jsparkSession.catalog().tableExists(f"{db_name}.{table_name}")):
    deltaTable = DeltaTable.forPath(spark, f"{folder_path}/{table_name}")
    deltaTable.alias("tgt").merge(
        input_df.alias("src"),
        merge_condition) \
      .whenMatchedUpdateAll()\
      .whenNotMatchedInsertAll()\
      .execute()
  else:
    input_df.write.mode("overwrite").partitionBy(partition_column).format("delta").saveAsTable(f"{db_name}.{table_name}")



