"""Módulo responsável por analisar compatibilidade de currículo com vagas usando Google Gemini."""
import os
import google.generativeai as genai


def analyze_job_match(resume_text: str, job_description: str, api_key: str = None) -> str:
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("GEMINI_API_KEY nao encontrada nas variaveis de ambiente ou parametros.")
    
    genai.configure(api_key=key)
    
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

    try:
        available_models = [
            m.name for m in genai.list_models() 
            if 'generateContent' in m.supported_generation_methods
        ]
    except Exception:
        available_models = []

    models_to_try = [m for m in available_models if 'flash' in m or 'pro' in m] + available_models + ["gemini-1.5-flash", "gemini-pro"]
    seen = set()
    models_to_try = [x for x in models_to_try if not (x in seen or seen.add(x))]

    last_error = None
    for m_name in models_to_try:
        try:
            clean_name = m_name.replace("models/", "")
            mod = genai.GenerativeModel(clean_name)
            response = mod.generate_content(prompt)
            return response.text
        except Exception as e:
            last_error = e
            continue
            
    raise RuntimeError(f"Nao foi possivel gerar conteudo com nenhum modelo Gemini disponivel. Ultimo erro: {last_error}")
