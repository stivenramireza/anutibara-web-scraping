import sys
sys.path.insert(0, "/usr/local/airflow/dags/scraping")
import scraping.script_paginator as PaginatorService
from datetime import datetime, timedelta
from airflow import DAG
from bs4 import BeautifulSoup
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

def print_task2(**kwargs):
    ti = kwargs['ti']
    pages_list = ti.xcom_pull(key=None, task_ids='generate_pages_urls')
    return pages_list

dag = DAG(
            dag_id='web-scraping',
            default_args=default_args,
            start_date=datetime.now(),
            schedule_interval=timedelta(minutes=720)
        )

pages_urls_task = PythonOperator(
            task_id='generate_pages_urls',
            python_callable=PaginatorService.paginate_properties,
            provide_context=True,
            dag=dag
        )

properties_urls_task = PythonOperator(
            task_id='generate_properties_urls',
            python_callable=print_task2,
            provide_context=True,
            dag=dag
        )

pages_urls_task >> properties_urls_task