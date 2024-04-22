from datetime import datetime
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator

def insert_data_function():
    for i in range(2,6):
        insert_data = PostgresOperator(
            task_id=f'insert_data_{i}',
            postgres_conn_id="postgres_localhost",
            sql=f'''INSERT INTO new_table (
                custom_id, timestamp, user_id 
                )
                VALUES
                ('{i+1}','2014-04-22 19:10:25-07', '{i+1}')
                ;'''
        )
        insert_data.execute(context=None)

dag_params = {
    'dag_id': 'PostgresOperator_dag',
    'start_date': datetime(2019, 10, 7),
    'schedule_interval': None
}

with DAG(**dag_params) as dag:

    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id="postgres_localhost",
        sql='''CREATE TABLE IF NOT EXISTS new_table (
            custom_id integer NOT NULL, timestamp TIMESTAMP NOT NULL, user_id VARCHAR (50) NOT NULL
            );''',
    )

    insert_data_function_task = PythonOperator(
        task_id='insert_data_function_task',
        python_callable=insert_data_function
    )

    create_table >> insert_data_function_task