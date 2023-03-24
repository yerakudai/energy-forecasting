from datetime import timedelta, datetime

from airflow.decorators import dag, task


@dag(
    dag_id="feature_pipeline",
    schedule=timedelta(hours=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["pipeline"]
)
def feature_pipeline():
    @task.virtualenv(
        task_id="run_feature_pipeline",
        requirements=["/opt/airflow/dags/feature_pipeline-0.1.0-py3-none-any.whl"],
        python_version="3.9",
        multiple_outputs=True,
        system_site_packages=False
    )
    def run_feature_pipeline():
        from feature_pipeline import run_feature_pipeline as _run_feature_pipeline

        return _run_feature_pipeline.run()

    @task.virtualenv(
        task_id="create_feature_view",
        requirements=["/opt/airflow/dags/feature_pipeline-0.1.0-py3-none-any.whl"],
        python_version="3.9",
        multiple_outputs=False,
        system_site_packages=False
    )
    def create_feature_view():
        from feature_pipeline import create_feature_view as _create_feature_view

        _create_feature_view.run()

    run_feature_pipeline() >> create_feature_view()


feature_pipeline()
