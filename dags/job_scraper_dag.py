"""DAG do Airflow para varredura automática de vagas e análise com Google Gemini (AI Job Matcher).

Roda duas vezes ao dia (9h e 18h):
1. Coleta/leitura de descrições de vagas.
2. Análise de compatibilidade (Match ATS) via Google Gemini.
3. Salvamento ou notificação dos melhores matches.
"""
import os
import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

if "/opt/airflow" not in sys.path:
    sys.path.insert(0, "/opt/airflow")

default_args = {
    "owner": "jessica",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def _run_job_matching(**context):
    from src.job_analyzer.matcher import analyze_job_match

    print("Iniciando varredura e analise de vagas com Google Gemini...")
    
    resume_path = "/app/resume.txt" if os.path.exists("/app/resume.txt") else "resume.txt"
    job_path = "/app/sample_job.txt" if os.path.exists("/app/sample_job.txt") else "sample_job.txt"

    if not os.path.exists(resume_path) or not os.path.exists(job_path):
        print("Arquivos de curriculo ou vaga nao encontrados.")
        return

    with open(resume_path, "r", encoding="utf-8") as f:
        resume_text = f.read()

    with open(job_path, "r", encoding="utf-8") as f:
        job_text = f.read()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY nao configurada nas variaveis de ambiente do Airflow.")
        return

    analise = analyze_job_match(resume_text, job_text, api_key=api_key)
    print("=== Resultado da Análise Automática de Vaga ===")
    print(analise)


with DAG(
    dag_id="job_scraper_gemini_pipeline",
    description="Varredura de vagas e analise de match com Gemini (9h e 18h)",
    default_args=default_args,
    schedule_interval="0 9,18 * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["carreira", "ai-job-matcher"],
) as dag:
    
    analyze_jobs = PythonOperator(
        task_id="analyze_jobs_with_gemini",
        python_callable=_run_job_matching,
    )
