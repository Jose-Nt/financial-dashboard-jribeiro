import streamlit as st
from time import sleep

st.set_page_config(
    page_title="Monitoramento Financeiro - Login",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    [data-testid="stHeader"] {
        display: none;
    }
    
    [data-testid="stToolbar"] {
        display: none;
    }

    [data-testid="stSidebarCollapsedControl"] {
        display: none;
    }

    .block-container {
        padding-top: 3rem;
        padding-bottom: 0rem;
    }
    
    .stApp {
        background: linear-gradient(to bottom, #126b86 27vh, #F4F6F8 23vh);
        background-attachment: fixed;
    }

    [data-testid="stSidebarNav"] {
        display: none;
    }

    .stButton > button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #126b86;
        color: white;
        border: none;
        font-weight: 600;
        box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2);
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #0e5063;
        transform: translateY(-2px);
        color: white;
    }
    
    .stTextInput input {
        background-color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)

if 'logado' not in st.session_state:
    st.session_state['logado'] = False

if 'login_error' not in st.session_state:
    st.session_state['login_error'] = False

def tentar_login():
    user = st.session_state.get("input_user")
    pw = st.session_state.get("input_senha")
    
    if user == "admin" and pw == "123":
        st.session_state['logado'] = True
        st.session_state['login_error'] = False 
        st.success("Login realizado com sucesso!")
        sleep(0.5)
        st.switch_page("pages/dashboard.py")
    else:
        st.session_state['login_error'] = True

col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    
    st.markdown(
        """
        <div style="display: flex; justify-content: center; padding-bottom: 6rem;">
            <img src="https://grupo-union-2.s3.amazonaws.com/sites/logos/14577.png" width="350">
        </div>
        """,
        unsafe_allow_html=True
    )
    
    with st.container(border=True):
        user = st.text_input("Usuário", key="input_user", placeholder="Digite seu usuário")
        senha = st.text_input("Senha", type="password", key="input_senha", placeholder="••••••")

    st.write("") 
    
    if st.button("ACESSAR SISTEMA"):
        tentar_login()

    if st.session_state['login_error']:
        st.error("Usuário ou senha incorretos.")

    st.markdown("<p style='text-align: center; color: #9CA3AF; font-size: 12px; margin-top: 20px;'>© 2025 J.Ribeiro Imóveis</p>", unsafe_allow_html=True)