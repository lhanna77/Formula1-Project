from google.cloud import bigquery
from json import load
from os import listdir
from shutil import copy2

# Create a BigQuery client
client = bigquery.Client()

def populate_tables(schema_folder_path = 'silver/table_schemas'):

    files = listdir(schema_folder_path)
    if schema_folder_path == 'gold/report_schemas':
        env = 'gold'
    else:
        env = 'silver'
    
    #files = ['race_results.json']

    for f in files:
        
        f=f.replace('.json','')

        # Define the table ID
        table_id = f'mstr-globalbi-sbx-c730.lh_f1_{env}.{f}'

        # Define the path to your JSON schema file and CSV data file
        schema_file_path = f'{schema_folder_path}/{f}.json'
        csv_file_path = f'{env}/{f}.csv'

        # Load the schema from JSON file
        try:
            with open(schema_file_path, 'r') as schema_file:
                schema = load(schema_file)
        except FileNotFoundError:
            print("Schema file not found. Please provide a valid schema file path.")
            exit()
            
        # Define the job config
        job_config = bigquery.LoadJobConfig(
            schema=schema,
            source_format=bigquery.SourceFormat.CSV,
            write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE,
            skip_leading_rows = 1,
            autodetect = False 
        )

        # Load data from CSV file
        try:
            with open(csv_file_path, 'rb') as source_file:
                job = client.load_table_from_file(source_file, table_id, job_config=job_config)

            # Wait for the job to complete
            job.result()
            print(f"{f} data loaded successfully - {job.output_rows} rows!")
        except FileNotFoundError:
            print("CSV file not found. Please provide a valid CSV file path.")
            exit()
        except Exception as e:
            print(f"An error occurred: {e}")
            exit()
            
            
if __name__ == '__main__':
    
    populate_tables()
    populate_tables(schema_folder_path = 'gold/report_schemas')