from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from datetime import datetime, timedelta
from reportlab.lib import colors
from io import BytesIO
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Monitoramento Financeiro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'logado' not in st.session_state or not st.session_state['logado']:
    st.warning("Por favor, faça login para acessar esta página.")
    st.stop()

st.markdown("""
<style>
    div.stButton > button {
        background-color: #126b86;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
        height: 3em; 
    }
    div.stButton > button:hover {
        background-color: #0e5063;
        color: white;
        transform: translateY(-2px);
    }
    
    .title-center {
        text-align: center;
        color: #126b86;
        font-weight: 700;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def gerar_dados_amplos():
    np.random.seed(42) 
    n_registros = 150
    
    nomes = ["João Silva", "Maria Oliveira", "Construtora Alpha", "Imobiliária Morada", "Pedro Santos", "Ana Costa", "Carlos Souza", "Fernanda Lima", "Roberto Almeida", "Júlia Pereira"]
    bancos = ["Banco do Brasil", "Itaú", "Bradesco", "Santander", "Caixa", "Nubank", "Inter"]
    
    datas = [datetime.now() - timedelta(days=np.random.randint(0, 60)) for _ in range(n_registros)]
    
    dados = {
        "Data": datas,
        "Nome": [np.random.choice(nomes) for _ in range(n_registros)],
        "Banco": [np.random.choice(bancos) for _ in range(n_registros)],
        "Agência": [f"{np.random.randint(1000, 9999)}" for _ in range(n_registros)],
        "Conta": [f"{np.random.randint(10000, 99999)}-{np.random.randint(1, 9)}" for _ in range(n_registros)],
        "Valor": np.random.uniform(150.00, 25000.00, n_registros)
    }
    
    df = pd.DataFrame(dados)
    return df.sort_values(by="Data", ascending=False)

def filtrar_dados(df, periodo_texto):
    dias_map = {
        "Últimos 7 dias": 7,
        "Últimos 15 dias": 15,
        "Últimos 30 dias": 30
    }
    dias = dias_map.get(periodo_texto, 30)
    data_corte = datetime.now() - timedelta(days=dias)
    return df[df['Data'] >= data_corte]

def gerar_pdf(df_display, periodo):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    
    elements.append(Paragraph(f"Relatório Financeiro: {periodo}", title_style))
    elements.append(Paragraph("<br/><br/>", styles['Normal']))
    
    data = [df_display.columns.to_list()] + df_display.values.tolist()
    
    table = Table(data)
    
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#126b86')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ])
    table.setStyle(style)
    
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer

def exibir_overlay_resultados(df, periodo):
    st.write("")
    st.markdown(f"### Relatório: {periodo}")
    
    with st.container(border=True):
        df_display = df.copy()
        df_display['Data'] = df_display['Data'].dt.strftime('%d/%m/%Y')
        df_display['Valor'] = df_display['Valor'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Nome": st.column_config.TextColumn("Nome Favorecido"),
                "Banco": st.column_config.TextColumn("Instituição"),
                "Valor": st.column_config.TextColumn("Valor (R$)"),
            }
        )
        
        total = df['Valor'].sum()
        st.markdown("---")
        c1, c2, c3 = st.columns([2, 2, 2])
        c1.metric("Total no Período", f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        c2.metric("Registros Encontrados", len(df))
        
        with c3:
            st.write("")
            pdf_bytes = gerar_pdf(df_display, periodo)
            st.download_button(
                label="📥 Baixar PDF",
                data=pdf_bytes,
                file_name=f"relatorio_financeiro_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

with st.sidebar:
    st.image("https://grupo-union-2.s3.amazonaws.com/sites/logos/14577.png", width=150)
    st.write(f"**Usuário:** Admin")
    st.divider()
    if st.button("Sair / Logout"):
        st.session_state['logado'] = False
        st.switch_page("app.py")

st.markdown("<h2 class='title-center'>Débitos não identificados</h2>", unsafe_allow_html=True)

with st.container(border=True):
    col_filtro1, col_filtro2 = st.columns([3, 1])

    with col_filtro1:
        periodo_selecionado = st.selectbox(
            "Selecione o Período",
            ["Últimos 7 dias", "Últimos 15 dias", "Últimos 30 dias"]
        )

    with col_filtro2:
        st.write("") 
        st.write("") 
        botao_pesquisar = st.button("PESQUISAR", use_container_width=True)

if botao_pesquisar:

    df_completo = gerar_dados_amplos()
    
    df_filtrado = filtrar_dados(df_completo, periodo_selecionado)
    
    exibir_overlay_resultados(df_filtrado, periodo_selecionado)