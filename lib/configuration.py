# Databricks notebook source

archive_bronze_folder_path = "files/archive"
archive_silver_folder_path = f"{archive_bronze_folder_path}/silver"

v_archive_data_source = "file"

bronze_folder_path = "files/latest_data_from_api"
silver_folder_path = f"{bronze_folder_path}/silver"
gold_folder_path = f"{bronze_folder_path}/gold"

v_data_source = "api"