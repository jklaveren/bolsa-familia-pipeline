"""Script CLI para analisar compatibilidade de vaga com o currículo usando Gemini."""
import argparse
import os
from dotenv import load_dotenv
from src.job_analyzer.matcher import analyze_job_match

load_dotenv()


def main() -> None:
    parser = argparse.ArgumentParser(description="Analisa match entre curriculo e vaga usando Gemini.")
    parser.add_argument("--resume", type=str, default="resume.txt", help="Caminho para arquivo de texto com o curriculo")
    parser.add_argument("--job", type=str, required=True, help="Caminho para arquivo de texto com a descricao da vaga")
    args = parser.parse_args()

    if not os.path.exists(args.resume):
        print(f"Erro: Arquivo de curriculo '{args.resume}' nao encontrado. Crie um arquivo com seu curriculo.")
        return

    if not os.path.exists(args.job):
        print(f"Erro: Arquivo de descricao da vaga '{args.job}' nao encontrado.")
        return

    with open(args.resume, "r", encoding="utf-8") as f:
        resume_text = f.read()

    with open(args.job, "r", encoding="utf-8") as f:
        job_text = f.read()

    print("Analisando compatibilidade com Gemini...")
    try:
        resultado = analyze_job_match(resume_text, job_text)
        print("\n=== Resultado da Análise ATS ===")
        print(resultado)
    except Exception as e:
        print(f"Erro na analise: {e}")


if __name__ == "__main__":
    main()
