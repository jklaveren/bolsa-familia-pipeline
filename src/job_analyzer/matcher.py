"""Módulo responsável por analisar compatibilidade, otimizar currículos e gerar cartas de apresentação com Google Gemini."""
import os
import google.generativeai as genai


def _get_active_model():
    """Retorna um modelo Gemini funcional listado dinamicamente."""
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
            return genai.GenerativeModel(clean_name)
        except Exception as e:
            last_error = e
            continue
    raise RuntimeError(f"Nenhum modelo Gemini disponivel. Erro: {last_error}")


def analyze_job_match(resume_text: str, job_description: str, api_key: str = None) -> str:
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("GEMINI_API_KEY nao encontrada nas variaveis de ambiente ou parametros.")
    
    genai.configure(api_key=key)
    mod = _get_active_model()
    
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
    response = mod.generate_content(prompt)
    return response.text


def tailor_resume(resume_text: str, job_description: str, api_key: str = None) -> str:
    """Reescreve o currículo do usuário otimizando-o especificamente para a vaga."""
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("GEMINI_API_KEY nao encontrada nas variaveis de ambiente ou parametros.")
    
    genai.configure(api_key=key)
    mod = _get_active_model()
    
    prompt = f"""
Atue como um redator profissional de currículos sênior e especialista em ATS.
Com base no currículo original e na descrição da vaga abaixo, reescreva e otimize o currículo para esta vaga específica.
Regras:
- Destaque as tecnologias e competências exigidas pela vaga que já constam no currículo original.
- Melhore a redação dos bullet points focando em impacto quantificável.
- Mantenha a veracidade das informações originais (não invente experiências).
- Retorne o currículo otimizado formatado em Markdown pronto para uso.

CURRÍCULO ORIGINAL:
{resume_text}

DESCRIÇÃO DA VAGA:
{job_description}
"""
    response = mod.generate_content(prompt)
    return response.text


def generate_cover_letter(resume_text: str, job_description: str, api_key: str = None) -> str:
    """Gera uma carta de apresentação personalizada para a vaga."""
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("GEMINI_API_KEY nao encontrada nas variaveis de ambiente ou parametros.")
    
    genai.configure(api_key=key)
    mod = _get_active_model()
    
    prompt = f"""
Atue como um profissional sênior de Engenharia de Dados escrevendo uma carta de apresentação altamente persuasiva para a vaga descrita abaixo.
Utilize o currículo como base para destacar os projetos e stack mais relevantes.
A carta deve ser profissional, direta, em tom entusiasmado e pronta para ser enviada a recrutadores ou anexada no LinkedIn.

CURRÍCULO:
{resume_text}

DESCRIÇÃO DA VAGA:
{job_description}
"""
    response = mod.generate_content(prompt)
    return response.text
