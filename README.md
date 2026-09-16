# Pipeline de Dados — Novo Bolsa Família

Pipeline de engenharia de dados ponta a ponta sobre os microdados públicos de
pagamentos do **Novo Bolsa Família** (Portal da Transparência / CGU): ingestão
e limpeza em **PySpark**, armazenamento em **Delta Lake**, transformação
analítica em **dbt** rodando no **Databricks**, orquestração em **Airflow** e
CI/CD no GitHub Actions.

> Documento de design técnico completo: [`docs/projeto_tecnico_pyspark_databricks.pdf`](docs/projeto_tecnico_pyspark_databricks.pdf).
> 📊 [dbt docs — linhagem e documentação dos modelos Gold](https://jklaveren.github.io/bolsa-familia-pipeline/)

## Arquitetura

```
Portal da Transparência (CGU)          Databricks Community Edition
  CSV mensal, ISO-8859-1        Power BI / Looker Studio (exportação)
        │ HTTPS, sem auth               ▲
        ▼                               │
┌───────────────┐   ┌───────────────┐   │   ┌──────────────────────┐
│ Bronze         │──▶│ Silver         │──▶│──▶│ Gold (dbt-databricks) │
│ PySpark        │   │ PySpark        │       │ staging → marts       │
│ Delta, raw     │   │ tipagem, dedup │       │ testes de schema      │
│ part. mes_comp │   │ pseudonimiz.   │       │                        │
│                │   │ part. uf       │       └──────────────────────┘
└───────────────┘   └───────────────┘
        ▲                    ▲                          ▲
        └────────────────────┴──────── Airflow (DAG mensal) ────┘
```

## O que está implementado

- **Bronze/Silver em PySpark**, validados com dados reais: 12 das 14
  competências trimestrais (mar/2023–jan/2026) já processadas, totalizando
  **242 milhões de linhas** — [evidência](docs/evidencias/).
- **Pseudonimização** do NIS via SHA-256, com o nome completo do beneficiário
  removido a partir da camada Silver (ver [LGPD e privacidade](#lgpd-e-privacidade)).
- **4 modelos Gold em dbt** (staging → marts) rodando contra o Databricks,
  com **13 testes declarativos passando** — [dbt run](docs/evidencias/fase5_dbt_run.txt) /
  [dbt test](docs/evidencias/fase5_dbt_test.txt).
- **CI no GitHub Actions** (pytest + dbt test) a cada push, com o gate
  validado deliberadamente: [prova de que ele falha quando um teste dbt
  quebra](docs/evidencias/fase8_ci_falha_de_proposito.txt).
- **DAG do Airflow** (`ingest_bronze → clean_silver → dbt_run → dbt_test →
  notify`) orquestrando o pipeline completo via Docker Compose.
- **Comparação VAR vs. rede neural** sobre a série histórica nacional —
  [primeiro resultado](docs/evidencias/secao10_comparacao_modelos.json),
  ainda com amostra parcial (12 de 14 competências).

## LGPD e privacidade

O dataset é público (Lei de Acesso à Informação), mas contém **NIS e nome
completo não mascarados** — dados pessoais na definição da LGPD (Lei
13.709/2018). Medidas adotadas:

- Camada **Bronze**: dado bruto, tratada como zona restrita — nunca exposta em
  dashboards ou consumo.
- Camada **Silver em diante**: NIS é pseudonimizado via `SHA-256(nis + salt)`;
  o nome completo do beneficiário **não é propagado** para nenhuma camada além
  da Bronze.
- Finalidade exclusivamente educacional/portfólio — este repositório **não
  deve ser usado para reidentificação de beneficiários**.

## Como reproduzir localmente

### Pré-requisitos

- Python 3.11, JDK 17
- No Windows: [`winutils.exe`](https://github.com/cdarlint/winutils) +
  `hadoop.dll` (Hadoop 3.3.x) em `HADOOP_HOME\bin` — requisito conhecido do
  Spark local em Windows, não relacionado ao dataset

### Setup

```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt

source scripts/env.sh          # bash — ajuste os caminhos de JDK/HADOOP_HOME
# ou: . .\scripts\env.ps1      # PowerShell

export BOLSA_FAMILIA_PSEUDONYM_SALT="defina-um-valor-secreto-aqui"
```

### Baixar os dados e rodar o pipeline

```bash
curl -o data/raw/202601_NovoBolsaFamilia.zip \
  https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/novo-bolsa-familia/202601_NovoBolsaFamilia.zip

python -m src.bronze.ingest --competencia 202601
python -m src.silver.clean --competencia 202601
```

### Testes

```bash
pytest -v
```

### Airflow (Docker Compose)

```bash
cp dbt/bolsa_familia/profiles.yml.example dbt/bolsa_familia/profiles.yml
# preencher .env com DATABRICKS_HOST / DATABRICKS_HTTP_PATH / DATABRICKS_TOKEN
docker compose up --build -d
```

## Stack tecnológico

| Componente | Ferramenta |
|---|---|
| Processamento distribuído | PySpark 3.5.1 |
| Formato de armazenamento | Delta Lake (`delta-spark` 3.2.0) |
| Transformação analítica | dbt (`dbt-databricks` 1.8.4) |
| Orquestração | Apache Airflow (Docker Compose) |
| Ambiente gerenciado | Databricks Free Edition |
| Testes | pytest + chispa (PySpark), testes nativos do dbt (Gold) |
| CI/CD | GitHub Actions |

## Decisões de design

- Spark roda em modo standalone local (não cluster distribuído) — suficiente
  para o volume processado (~20M linhas/competência), sem custo de infra.
- Airflow local via Docker Compose demonstra domínio da ferramenta (DAGs,
  operators, scheduling, retries); é uma camada diferente de operar Airflow
  gerenciado (MWAA, Cloud Composer) em produção multi-time.
- A série histórica usa amostragem trimestral, não as ~35 competências
  completas disponíveis (~70GB) — decisão de escopo por limitação de disco,
  documentada na Seção 16 do design doc.

## Autora

Jessica Van Klaveren — projeto de portfólio para posições de Engenharia de
Dados Nível Pleno.
