import script_paginator as PaginatorService
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

def print_task2():
    print('-> Test passed')

dag = DAG(
            dag_id='web-scraping',
            default_args=default_args,
            start_date=datetime(2019,10,9),
            schedule_interval=timedelta(minutes=720)
        )

op_script_paginator = PythonOperator(
            task_id='script_paginator',
            python_callable=PaginatorService.main,
            dag=dag
        )

op_script_properties = PythonOperator(
            task_id='script_properties',
            python_callable=print_task2,
            dag=dag
        )

op_script_paginator >> op_script_properties