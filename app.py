import streamlit as st
import pandas as pd
from ferramenta import buscar_cep, buscar_tempo

# 1. Configuração da Página
st.set_page_config(
    page_title="SuperCEP Meteorologia",
    page_icon="🌦️",
    layout="wide"
)

# 2. Estilização CSS Customizada (Visual Moderno/Glassmorphism)
st.markdown("""
<style>
/* Fundo principal da aplicação */
.stApp {
    background: linear-gradient(135deg, #050b1e, #0a1931, #153066);
    color: #f8fafc;
}

/* Sidebar Estilizada */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #06283d, #1363df);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}

/* Forçar textos da Sidebar a ficarem brancos */
[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* Inputs da Sidebar */
.stTextInput input {
    background-color: rgba(255, 255, 255, 0.1) !important;
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 10px !important;
}

/* Customização dos Títulos Principais no Corpo */
.app-title {
    text-align: center;
    font-size: 45px;
    font-weight: 800;
    background: linear-gradient(45deg, #38bdf8, #0ea5e9, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
}

.app-subtitle {
    text-align: center;
    font-size: 18px;
    color: #94a3b8;
    margin-bottom: 40px;
}

/* Cards com efeito de vidro (Glassmorphism) */
.custom-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 25px;
    border-radius: 16px;
    backdrop-filter: blur(12px);
    margin-bottom: 25px;
}

.custom-card h3 {
    color: #38bdf8 !important;
    margin-top: 0;
    margin-bottom: 15px;
}

/* Ajuste nos containers de Métricas do Streamlit */
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 15px;
    border-radius: 12px;
}

/* Botão de Busca */
.stButton button {
    width: 100%;
    background: #0ea5e9;
    color: white !important;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    height: 45px;
    transition: all 0.3s ease;
}

.stButton button:hover {
    background: #0284c7;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(14, 165, 233, 0.4);
}
</style>
""", unsafe_allow_html=True)

# 3. Construção da Sidebar
st.sidebar.title("🌦️ SuperCEP")
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📍 Consulta Inteligente
Digite um CEP ao lado para mapear e monitorar o clima da região em tempo real.
""")

cep = st.sidebar.text_input('Digite o CEP (apenas números):', max_chars=8)
st.sidebar.markdown("---")

# Tentativa de carregar a logo de forma segura
try:
    st.sidebar.image('logo.png', use_container_width=True)
except:
    pass

# 4. Cabeçalho Principal (Corpo da Página)
st.markdown('<h1 class="app-title">🌦️ SuperCEP Meteorologia</h1>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">Consulte CEPs e acompanhe a previsão do tempo detalhada em tempo real</p>', unsafe_allow_html=True)

# 5. Lógica de Busca e Exibição dos Resultados
if st.sidebar.button("Buscar"):
    if not cep or len(cep) < 8:
        st.warning("⚠️ Por favor, insira um CEP válido com 8 dígitos.")
    else:
        with st.spinner("🌎 Localizando endereço e checando os céus..."):
            dados_cep = buscar_cep(cep)
            
            # Validação para caso a API não retorne dados válidos
            if not dados_cep or "erro" in dados_cep:
                st.error("❌ CEP não encontrado. Verifique os números e tente novamente.")
            else:
                # Layout em duas colunas: Esquerda (Endereço) / Direita (Métricas rápidas)
                col1, col2 = st.columns([1.2, 2])
                
                with col1:
                    # Mapeia as chaves da sua API (atendendo tanto minúsculas quanto padrões comuns)
                    rua = dados_cep.get("address", dados_cep.get("address_name", "Não informado"))
                    bairro = dados_cep.get("district", dados_cep.get("bairro", "Não informado"))
                    cidade = dados_cep.get("city", dados_cep.get("cidade", "Não informado"))
                    estado = dados_cep.get("state", dados_cep.get("estado", ""))
                    
                    st.markdown(f"""
                    <div class="custom-card">
                        <h3>📍 Localização Encontrada</h3>
                        <p style="margin: 8px 0;"><b>Logradouro:</b> {rua}</p>
                        <p style="margin: 8px 0;"><b>Bairro:</b> {bairro}</p>
                        <p style="margin: 8px 0;"><b>Cidade/UF:</b> {cidade} - {estado}</p>
                        <p style="margin: 8px 0;"><b>CEP de Origem:</b> {dados_cep.get("cep")}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
                    m_col1, m_col2, m_col3 = st.columns(3)
                    m_col1.metric("Latitude", dados_cep.get("lat", "N/A"))
                    m_col2.metric("Longitude", dados_cep.get("lng", "N/A"))
                    m_col3.metric("DDD Região", dados_cep.get("ddd", "N/A"))
                
                # Se houver coordenadas, busca e renderiza o clima
                if dados_cep.get("lat") and dados_cep.get("lng"):
                    try:
                        lat = float(dados_cep.get("lat"))
                        lng = float(dados_cep.get("lng"))
                        dados_clima = buscar_tempo(lat, lng)
                        
                        if "daily" in dados_clima:
                            chance_chuva = pd.DataFrame(dados_clima["daily"])
                            
                            # Tradução e renomeação amigável das colunas para exibição gráfica
                            chance_chuva.rename(columns={
                                "time": "Data", 
                                "precipitation_probability_max": "Probabilidade de Chuva (%)"
                            }, inplace=True)
                            
                            st.markdown("---")
                            st.subheader("📊 Probabilidade Máxima de Chuva para os Próximos Dias")
                            
                            # Gráfico de barras nativo bem distribuído
                            st.bar_chart(data=chance_chuva, x="Data", y="Probabilidade de Chuva (%)", color="#0ea5e9")
                            
                            # Exibição dos dados consolidados em formato dataframe moderno
                            st.subheader("📋 Tabela Preditiva Temporal")
                            st.dataframe(chance_chuva, use_container_width=True, hide_index=True)
                        else:
                            st.info("ℹ️ Dados de previsão diária indisponíveis para esta coordenada no momento.")
                    except Exception as e:
                        st.error(f"⚠️ Erro ao processar informações meteorológicas: {e}")