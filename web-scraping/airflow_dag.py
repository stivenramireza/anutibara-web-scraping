import sys
sys.path.insert(0, "/usr/local/airflow/dags/scraping")
import scraping.script_paginator as PaginatorService
import scraping.script_properties as PropertyService
import scraping.script_scraping as ScrapingService
import scraping.script_database as DatabaseService
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import os

default_args = {
    'owner': 'anutibara',
    'depends_on_past': False,
    'email': ['stivenramireza@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 5,
    'retry_delay': timedelta(seconds = 10)
}

dag = DAG(
    dag_id='web-scraping',
    default_args=default_args,
    start_date=datetime.now(),
    schedule_interval=timedelta(minutes=720),
)

url_pages_task = PythonOperator(
    task_id='load_url_pages',
    python_callable=PaginatorService.paginate_properties,
    dag=dag
)

url_properties_task = PythonOperator(
    task_id='load_url_properties',
    provide_context=True,
    python_callable=PropertyService.request_properties,
    dag=dag
)

scrape_property_db_task = PythonOperator(
    task_id='scrape_property_and_load_db',
    provide_context=True,
    priority_weight=10000,
    pool='scraper_pool',
    queue='default',
    python_callable=ScrapingService.scrape,
    dag=dag
)

url_pages_task >> url_properties_task >> scrape_property_db_task