# Databricks notebook source

from datetime import date
from pyspark.sql import SparkSession
from pandas import ExcelWriter,read_csv
from pathlib import Path
from os import path,listdir,unlink,mkdir
from shutil import rmtree
from requests import request
from csv import reader as csv_reader, writer as csv_writer
from lib import configuration

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

def call_api(url, limit=1000, offset=0):
  
  json_url = url + f'.json?limit={limit}&offset={offset}'
  response = request("GET", json_url)

  return response.json()

def write_api_results_to_json(file_type,output_file,all_rows_df):
    
    if file_type == 'json':
        jsonl_str = all_rows_df.to_json(orient='records',lines=True,force_ascii=False)
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(jsonl_str.replace('\/','/'))
            print(f'File - {output_file} populated from API') 

def get_max_result_id():
  
  # Specify the path to your CSV file and the column name
  csv_file_path = f'{configuration.silver_folder_path}/results.csv'
  column_name = 'result_id'

  # Read the CSV file into a DataFrame
  df = read_csv(csv_file_path)

  # Find the maximum value in the specified column
  max_value = df[column_name].max()

  print(f"The maximum value in the column '{column_name}' is: {max_value}")
  
  return max_value

def remove_old_api_files():
  
  folder_path = configuration.results_folder_path

  # Iterate over the contents of the directory
  for filename in listdir(folder_path):
      file_path = path.join(folder_path, filename)
      try:
          if path.isfile(file_path) or path.islink(file_path):
              unlink(file_path) # Remove the file or symbolic link
          elif path.isdir(file_path):
              rmtree(file_path, ignore_errors=True) # Remove the directory and its contents
              print(f'Directory - {folder_path} contents deleted')
      except Exception as e:
          print(f'Failed to delete {file_path}. Reason: {e}')
          
def create_inc_results_folder():
  
  folder_path = configuration.inc_results_folder_path

  # Create folder directory
  try:
    mkdir(folder_path)
    print(f'Directory - {folder_path} created')
  except FileExistsError:
    print(f'The directory - {folder_path} already exists')
  except Exception as e:
    print(f'An error occurred: {e}')


##################


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



