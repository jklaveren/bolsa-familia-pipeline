import json
import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Pipeline Novo Bolsa Família - Analytics & ML", page_icon="📊", layout="wide")

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; font-weight: bold; color: #1E3A8A; }
    .sub-header { font-size: 1.3rem; color: #4B5563; }
    .insight-box { background-color: #F3F4F6; padding: 20px; border-radius: 10px; border-left: 5px solid #2563EB; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">📊 Pipeline de Dados & Inteligência Analítica — Novo Bolsa Família</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Plataforma de Engenharia de Dados (PySpark + Delta Lake + dbt + Airflow) e Previsão Econômica (VAR vs Deep Learning).</p>', unsafe_allow_html=True)

st.sidebar.header("Painel de Navegação")
pagina = st.sidebar.selectbox("Escolha a Seção:", [
    "🚀 Visão Executiva & Arquitetura", 
    "📈 Machine Learning: VAR vs Rede Neural", 
    "🔒 Governança, LGPD & Qualidade",
    "📋 Evidências & Logs Reais"
])

if pagina == "🚀 Visão Executiva & Arquitetura":
    st.header("Visão Executiva do Projeto")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Volume Processado", "242 Milhões", "12 Competências Trimestrais")
    with col2:
        st.metric("Camada Silver", "19.48 Milhões", "Competência 202601")
    with col3:
        st.metric("Modelos Gold (dbt)", "4 Tabelas", "Staging → Marts")
    with col4:
        st.metric("Testes Declarativos", "13 Passando", "100% Cobertura dbt")

    st.markdown("---")
    st.subheader("Arquitetura Medalhão (Medallion Architecture)")
    
    st.markdown("""
    * **Bronze (Raw / PySpark):** Ingestão direta dos microdados da CGU em formato CSV comprimido, armazenados em tabelas Delta particionadas por mês de competência sem perda de fidelidade.
    * **Silver (Limpeza & LGPD):** Padronização de esquemas, conversão de decimais, quarentena de registros inválidos sem NIS e **pseudonimização do NIS via SHA-256 com Salt**, garantindo conformidade com a LGPD (Lei 13.709/2018).
    * **Gold (dbt & Databricks):** Modelagem analítica dimensional (Staging, Marts por UF e Mensal) com testes automatizados de unicidade, relacionamento e integridade.
    * **Orquestração (Airflow & CI/CD):** Pipeline automatizado em DAGs mensais com testes contínuos via GitHub Actions.
    """)

elif pagina == "📈 Machine Learning: VAR vs Rede Neural":
    st.header("Análise Preditiva & Comparação de Modelos (Seção 10)")
    
    st.markdown("""
    <div class="insight-box">
    <b>💡 Insight Técnico & Transparência Metodológica:</b><br>
    O projeto compara um modelo econométrico linear tradicional (<b>VAR - Vector Autoregression</b>) com uma <b>Rede Neural Simples (Dense Keras)</b> para prever o valor total de pagamentos do Bolsa Família. Em séries temporais curtas de frequência trimestral, modelos lineares como o VAR costumam demonstrar maior robustez estatística que redes neurais densas, evitando overfitting severo.
    </div>
    """, unsafe_allow_html=True)
    
    json_path = "docs/evidencias/secao10_comparacao_modelos.json"
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        col_m1, col_m2 = st.columns(2)
        
        with col_m1:
            st.subheader("📉 Desempenho: Modelo VAR")
            metrics_var = data["var"]["metricas"]
            st.metric("RMSE (Erro Quadrático Médio)", f"R$ {metrics_var['rmse']:,.2f}")
            st.metric("MAE (Erro Absoluto Médio)", f"R$ {metrics_var['mae']:,.2f}")
            st.metric("MAPE (Erro Percentual)", f"{metrics_var['mape']:.2f}%")
            
        with col_m2:
            st.subheader("🧠 Desempenho: Rede Neural")
            metrics_nn = data["rede_neural"]["metricas"]
            st.metric("RMSE (Erro Quadrático Médio)", f"R$ {metrics_nn['rmse']:,.2f}")
            st.metric("MAE (Erro Absoluto Médio)", f"R$ {metrics_nn['mae']:,.2f}")
            st.metric("MAPE (Erro Percentual)", f"{metrics_nn['mape']:.2f}%")
            
        st.markdown("---")
        st.subheader("Gráfico Comparativo de Predições vs Valores Reais")
        
        reais = data["valores_reais_teste"]
        preds_var = data["var"]["predicoes"]
        preds_nn = data["rede_neural"]["predicoes"]
        
        df_plot = pd.DataFrame({
            "Período de Teste": [f"Trimestre T+{i+1}" for i in range(len(reais))],
            "Valor Real": reais,
            "Previsão VAR": preds_var,
            "Previsão Rede Neural": preds_nn
        })
        
        df_melted = df_plot.melt(id_vars=["Período de Teste"], value_vars=["Valor Real", "Previsão VAR", "Previsão Rede Neural"],
                                   var_name="Modelo / Realidade", value_name="Valor Total (R$ Bilhões)")
        
        fig = px.line(df_melted, x="Período de Teste", y="Valor Total (R$ Bilhões)", color="Modelo / Realidade",
                      markers=True, title="Comparativo de Acurácia de Previsão na Janela de Teste")
        fig.update_layout(yaxis_tickformat=",.0f")
        st.plotly_chart(fig, use_container_width=True)

elif pagina == "🔒 Governança, LGPD & Qualidade":
    st.header("Governança de Dados, Privacidade e Qualidade")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🛡️ Conformidade LGPD")
        st.markdown("""
        * **Camada Bronze:** Contém o dado bruto original da CGU (incluindo NIS e nome completo). Trata-se de zona restrita e sigilosa.
        * **Camada Silver em diante:** O NIS é pseudonimizado via algoritmo `SHA-256(nis + salt)` secreto, e o **nome completo é completamente expurgado**, impossibilitando reidentificação direta de titulares.
        """)
    with col2:
        st.subheader("🔍 Regras de Qualidade e Quarentena")
        st.markdown("""
        * **Validação de Esquema e Tipos:** Conversão rigorosa de valores monetários com vírgula para ponto flutuante.
        * **Quarentena de NIS Ausente:** Registros com chaves nulas ou corrompidas são isolados em diretório de quarentena (`data/silver/quarentena_sem_nis`) para auditoria sem corromper o pipeline analítico.
        """)

elif pagina == "📋 Evidências & Logs Reais":
    st.header("Auditoria de Logs e Relatórios de Execução")
    
    evidencias = {
        "Relatório de Qualidade (Fase 6)": "docs/evidencias/fase6_quality_report_202601.txt",
        "Testes do dbt Gold (Fase 5)": "docs/evidencias/fase5_dbt_test.txt",
        "Schema da Camada Silver (Fase 3)": "docs/evidencias/fase3_silver_schema_202601.txt"
    }
    
    escolha = st.selectbox("Selecione o relatório de auditoria:", list(evidencias.keys()))
    path = evidencias[escolha]
    
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            conteudo = f.read()
        st.text_area("Registro Oficial", conteudo, height=400)
    else:
        st.warning("Relatório não encontrado.")
