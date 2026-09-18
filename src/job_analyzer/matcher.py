"""Módulo responsável por analisar compatibilidade de currículo com vagas usando Google Gemini."""
import os
import google.generativeai as genai


def analyze_job_match(resume_text: str, job_description: str, api_key: str = None) -> str:
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("GEMINI_API_KEY nao encontrada nas variaveis de ambiente ou parametros.")
    
    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
Atue como um recrutador técnico especialista em ATS (Applicant Tracking System) e Engenharia de Dados.
Compare o currículo abaixo com a descrição da vaga e forneça uma análise estruturada em Markdown contendo:
1. **Nota de Match (0 a 100):** Avaliação de compatibilidade geral.
2. **Palavras-chave Cruciais Faltantes:** Termos técnicos da vaga que não estão claros no currículo.
3. **Pontos Fortes:** O que já está excelente e alinhado no currículo.
4. **Recomendações Práticas:** O que alterar ou adicionar no currículo para passar no ATS desta vaga específica.

CURRÍCULO:
{resume_text}

DESCRIÇÃO DA VAGA:
{job_description}
"""

    response = model.generate_content(prompt)
    return response.text
