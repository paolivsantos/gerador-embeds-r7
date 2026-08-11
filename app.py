import streamlit as st

# Configuração da Página
st.set_page_config(
    page_title="Gerador de Embeds - R7 Esportes",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ Gerador de Embeds Diretos - R7 Esportes")
st.markdown("Ferramenta para a redação gerar o bloco HTML pronto para colar direto no CMS (sem precisar de arquivos externos).")

# --- BARRA LATERAL (CONFIGURAÇÃO) ---
st.sidebar.header("Configuração do Sorteio")

campeonato = st.sidebar.selectbox(
    "Selecione o Campeonato",
    ["CONMEBOL Libertadores", "Copa do Brasil", "Copa Sul-Americana"]
)

fase = st.sidebar.selectbox(
    "Selecione a Fase",
    ["Fase de Grupos (Potes e Grupos)", "Oitavas de Final (Pote Único)", "Quartas de Final (Pote Único)"]
)

st.sidebar.markdown("---")
st.sidebar.info("Preencha os campos ao lado com os nomes dos times separados por vírgula.")

# --- ÁREA PRINCIPAL DE ENTRADA DE DADOS ---
st.header(f"Parâmetros: {campeonato} - {fase}")

dados_input = {}

if "Fase de Grupos" in fase:
    st.subheader("1. Potes de Origem")
    col1, col2 = st.columns(2)
    with col1:
        dados_input["pote1"] = st.text_area("Pote 1 (Sep. por vírgula)", "Flamengo (BRA), Palmeiras (BRA), Boca Juniors (ARG), Peñarol (URU), Nacional (URU), Liga de Quito (ECU), Fluminense (BRA), Independiente del Valle (ECU)")
        dados_input["pote2"] = st.text_area("Pote 2 (Sep. por vírgula)", "Lanús (ARG), Libertad (PAR), Estudiantes (ARG), Cerro Porteño (PAR), Corinthians (BRA), Bolívar (BOL), Cruzeiro (BRA), Universitario (PER)")
    with col2:
        dados_input["pote3"] = st.text_area("Pote 3 (Sep. por vírgula)", "Junior (COL), U. Católica (CHI), Rosario Central (ARG), Santa Fe (COL), Always Ready (BOL), Coquimbo (CHI), La Guaira (VEN), Cusco (PER)")
        dados_input["pote4"] = st.text_area("Pote 4 (Sep. por vírgula)", "U. Central (VEN), Platense (ARG), Ind. Rivadavia (ARG), Mirassol (BRA), Ind. Medellín (COL), Tolima (COL), Sporting Cristal (PER), Barcelona (ECU)")

    st.subheader("2. Grupos de Destino (A ao H)")
    g_col1, g_col2, g_col3, g_col4 = st.columns(4)
    with g_col1:
        dados_input["grupoA"] = st.text_input("Grupo A", "Flamengo (BRA), Lanús (ARG), Junior (COL), Mirassol (BRA)")
        dados_input["grupoB"] = st.text_input("Grupo B", "Palmeiras (BRA), Libertad (PAR), U. Católica (CHI), Platense (ARG)")
    with g_col2:
        dados_input["grupoC"] = st.text_input("Grupo C", "Boca Juniors (ARG), Estudiantes (ARG), Rosario Central (ARG), Tolima (COL)")
        dados_input["grupoD"] = st.text_input("Grupo D", "Peñarol (URU), Cerro Porteño (PAR), Santa Fe (COL), Ind. Medellín (COL)")
    with g_col3:
        dados_input["grupoE"] = st.text_input("Grupo E", "Nacional (URU), Corinthians (BRA), Always Ready (BOL), Ind. Rivadavia (ARG)")
        dados_input["grupoF"] = st.text_input("Grupo F", "Liga de Quito (ECU), Bolívar (BOL), Coquimbo (CHI), U. Central (VEN)")
    with g_col4:
        dados_input["grupoG"] = st.text_input("Grupo G", "Fluminense (BRA), Cruzeiro (BRA), La Guaira (VEN), Sporting Cristal (PER)")
        dados_input["grupoH"] = st.text_input("Grupo H", "Ind. del Valle (ECU), Universitario (PER), Cusco (PER), Barcelona (ECU)")

elif "Oitavas de Final" in fase:
    dados_input["poteUnico"] = st.text_area("Times Classificados (Pote Único)", "Palmeiras, Flamengo, São Paulo, Botafogo, Atlético-MG, Bahia, Fluminense, Grêmio, Internacional, Cruzeiro, Corinthians, Vasco, Fortaleza, Cuiabá, Athletico-PR, Bragantino")
    
    st.subheader("Confrontos (Ida e Volta)")
    chaves_cols = st.columns(2)
    dados_input["chaves"] = []
    for i in range(1, 9):
        with chaves_cols[(i-1)%2]:
            val = st.text_input(f"Confronto {i} (Ex: Time A, Time B)", f"Time A{i}, Time B{i}")
            dados_input["chaves"].append(val)

elif "Quartas de Final" in fase:
    dados_input["poteUnico"] = st.text_area("Times Classificados (Pote Único)", "Palmeiras, Santos, Vasco, Atlético-MG, Cruzeiro, Grêmio, Internacional, Vitória")
    
    st.subheader("Confrontos (Ida e Volta)")
    chaves_cols = st.columns(2)
    dados_input["chaves"] = []
    for i in range(1, 5):
        with chaves_cols[(i-1)%2]:
            val = st.text_input(f"Confronto {i} (Ex: Time A, Time B)", f"Time A{i}, Time B{i}")
            dados_input["chaves"].append(val)

# --- BOTÃO DE GERAÇÃO DO CÓDIGO ---
st.markdown("---")
if st.button("🚀 Gerar Bloco HTML para o CMS", type="primary", use_container_width=True):
    
    def gerar_itens_html(texto_virgula):
        itens = [x.strip() for x in texto_virgula.split(",") if x.strip()]
        html_out = ""
        for idx, item in enumerate(itens):
            html_out += f'<div class="r7-item-lista"><span class="r7-pos">{idx+1}</span><span class="r7-time-txt">{item}</span></div>\n'
        return html_out

    titulo_pagina = f"{campeonato} - {fase}"
    
    # Bloco HTML encapsulado com escopo seguro (sem afetar a página pai e travado em 780px)
    html_gerado = f"""<!-- INICIO EMBED SORTEIO R7 -->
<style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&family=Roboto+Condensed:wght@400;700&display=swap');
    
    #r7-sorteio-wrapper {{
        width: 100%;
        max-width: 780px;
        margin: 0 auto;
        background: radial-gradient(circle at center top, #063614 0%, #020a05 80%);
        color: #fff;
        font-family: 'Roboto Condensed', sans-serif;
        padding: 20px 15px;
        border-radius: 8px;
        box-sizing: border-box;
    }}
    #r7-sorteio-wrapper *, #r7-sorteio-wrapper *::before, #r7-sorteio-wrapper *::after {{
        box-sizing: border-box;
    }}
    #r7-sorteio-wrapper header {{ text-align: center; margin-bottom: 25px; }}
    #r7-sorteio-wrapper .r7-logo-header {{ display: flex; align-items: center; justify-content: center; gap: 12px; font-family: 'Oswald', sans-serif; font-size: 2rem; text-transform: uppercase; }}
    #r7-sorteio-wrapper .r7-logo-r7 {{ background: #08E148; color: #000; padding: 2px 10px; border-radius: 4px; font-weight: 900; }}
    #r7-sorteio-wrapper .r7-title-sorteio {{ font-size: 1.4rem; letter-spacing: 1px; color: #fff; font-weight: bold; text-transform: uppercase; font-family: 'Oswald', sans-serif; margin-top: 5px; }}
    #r7-sorteio-wrapper .r7-section-header {{ font-family: 'Oswald', sans-serif; text-transform: uppercase; font-size: 1.2rem; letter-spacing: 2px; margin: 25px 0 12px; text-align: center; padding-bottom: 6px; }}
    #r7-sorteio-wrapper .r7-grid-layout {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }}
    #r7-sorteio-wrapper .r7-potes-header {{ color: #c5a059; border-bottom: 2px solid #c5a059; }}
    #r7-sorteio-wrapper .r7-grupos-header, #r7-sorteio-wrapper .r7-confrontos-header {{ color: #08E148; border-bottom: 2px solid #08E148; }}
    #r7-sorteio-wrapper .r7-card {{ background: rgba(0, 0, 0, 0.6); backdrop-filter: blur(10px); border-radius: 6px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.05); height: fit-content; }}
    #r7-sorteio-wrapper .r7-card-header {{ font-family: 'Oswald', sans-serif; text-align: center; padding: 10px; font-weight: bold; text-transform: uppercase; font-size: 1rem; }}
    #r7-sorteio-wrapper .r7-item-lista {{ display: flex; align-items: center; padding: 10px 12px; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.9rem; }}
    #r7-sorteio-wrapper .r7-item-lista:last-child {{ border: none; }}
    #r7-sorteio-wrapper .r7-pos {{ width: 22px; height: 22px; display: flex; align-items: center; justify-content: center; border-radius: 50%; font-size: 0.75rem; margin-right: 10px; font-weight: bold; }}
    #r7-sorteio-wrapper .r7-time-txt {{ font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; }}
    
    #r7-sorteio-wrapper .r7-card.r7-pote {{ border: 1px solid rgba(197, 160, 89, 0.3); }}
    #r7-sorteio-wrapper .r7-card.r7-pote .r7-card-header {{ background: linear-gradient(to right, #6e5221, #c5a059, #6e5221); color: #000; }}
    #r7-sorteio-wrapper .r7-card.r7-pote .r7-pos {{ background: rgba(197, 160, 89, 0.15); color: #c5a059; border: 1px solid #c5a059; }}

    #r7-sorteio-wrapper .r7-card.r7-grupo, #r7-sorteio-wrapper .r7-card.r7-confronto {{ border: 1px solid rgba(8, 225, 72, 0.4); }}
    #r7-sorteio-wrapper .r7-card.r7-grupo .r7-card-header, #r7-sorteio-wrapper .r7-card.r7-confronto .r7-card-header {{ background: linear-gradient(to right, #031a0b, #0a4d20, #031a0b); color: #08E148; border-bottom: 2px solid #08E148; }}
    #r7-sorteio-wrapper .r7-card.r7-grupo .r7-pos, #r7-sorteio-wrapper .r7-card.r7-confronto .r7-pos {{ background: rgba(8, 225, 72, 0.2); color: #08E148; border: 1px solid #08E148; }}
    
    #r7-sorteio-wrapper .r7-tag-jogo {{ font-size: 0.6rem; padding: 2px 4px; border-radius: 3px; margin-right: 8px; font-weight: bold; min-width: 38px; text-align: center; }}
    #r7-sorteio-wrapper .r7-ida {{ background: #08E148; color: #000; }}
    #r7-sorteio-wrapper .r7-volta {{ background: #fff; color: #000; }}
    #r7-sorteio-wrapper .r7-vs {{ margin: 0 6px; color: #08E148; font-style: italic; font-size: 0.75rem; font-weight: bold; }}
    
    @media (max-width: 600px) {{
        #r7-sorteio-wrapper .r7-grid-layout {{ grid-template-columns: 1fr; }}
        #r7-sorteio-wrapper .r7-pote-times-grid {{ grid-template-columns: repeat(2, 1fr) !important; }}
    }}
</style>

<div id="r7-sorteio-wrapper">
    <header>
        <div class="r7-logo-header"><span class="r7-logo-r7">R7</span> ESPORTES</div>
        <div class="r7-title-sorteio">{titulo_pagina}</div>
    </header>
"""

    if "Fase de Grupos" in fase:
        html_gerado += f"""
    <div class="r7-section-header r7-potes-header">Potes do Sorteio</div>
    <div class="r7-grid-layout">
        <div class="r7-card r7-pote"><div class="r7-card-header">Pote 1</div>{gerar_itens_html(dados_input["pote1"])}</div>
        <div class="r7-card r7-pote"><div class="r7-card-header">Pote 2</div>{gerar_itens_html(dados_input["pote2"])}</div>
        <div class="r7-card r7-pote"><div class="r7-card-header">Pote 3</div>{gerar_itens_html(dados_input["pote3"])}</div>
        <div class="r7-card r7-pote"><div class="r7-card-header">Pote 4</div>{gerar_itens_html(dados_input["pote4"])}</div>
    </div>

    <div class="r7-section-header r7-grupos-header">Grupos da Competição</div>
    <div class="r7-grid-layout">
        <div class="r7-card r7-grupo"><div class="r7-card-header">Grupo A</div>{gerar_itens_html(dados_input["grupoA"])}</div>
        <div class="r7-card r7-grupo"><div class="r7-card-header">Grupo B</div>{gerar_itens_html(dados_input["grupoB"])}</div>
        <div class="r7-card r7-grupo"><div class="r7-card-header">Grupo C</div>{gerar_itens_html(dados_input["grupoC"])}</div>
        <div class="r7-card r7-grupo"><div class="r7-card-header">Grupo D</div>{gerar_itens_html(dados_input["grupoD"])}</div>
        <div class="r7-card r7-grupo"><div class="r7-card-header">Grupo E</div>{gerar_itens_html(dados_input["grupoE"])}</div>
        <div class="r7-card r7-grupo"><div class="r7-card-header">Grupo F</div>{gerar_itens_html(dados_input["grupoF"])}</div>
        <div class="r7-card r7-grupo"><div class="r7-card-header">Grupo G</div>{gerar_itens_html(dados_input["grupoG"])}</div>
        <div class="r7-card r7-grupo"><div class="r7-card-header">Grupo H</div>{gerar_itens_html(dados_input["grupoH"])}</div>
    </div>
        """
    else:
        pote_unico_itens = [x.strip() for x in dados_input["poteUnico"].split(",") if x.strip()]
        html_pote_grid = "".join([f'<div style="background: rgba(197, 160, 89, 0.1); border: 1px solid rgba(197, 160, 89, 0.3); padding: 8px; border-radius: 4px; text-align: center; font-weight: bold; text-transform: uppercase; font-size: 0.85rem;">{t}</div>' for t in pote_unico_itens])
        
        html_gerado += f"""
    <div class="r7-section-header r7-potes-header">Equipes Classificadas (Pote Único)</div>
    <div class="r7-card r7-pote" style="margin-bottom: 25px;">
        <div class="r7-card-header">Pote Único</div>
        <div class="r7-pote-times-grid" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; padding: 12px;">
            {html_pote_grid}
        </div>
    </div>

    <div class="r7-section-header r7-confrontos-header">Confrontos Definidos</div>
    <div class="r7-grid-layout">
        """
        
        for idx, chave_str in enumerate(dados_input["chaves"]):
            partes = [p.strip() for p in chave_str.split(",")]
            t1 = partes[0] if len(partes) > 0 else "Time A"
            t2 = partes[1] if len(partes) > 1 else "Time B"
            
            html_gerado += f"""
        <div class="r7-card r7-confronto">
            <div class="r7-card-header">Confronto {idx+1}</div>
            <div class="r7-item-lista"><span class="r7-tag-jogo r7-ida">IDA</span><span class="r7-time-txt">{t1}</span> <span class="r7-vs">X</span> <span class="r7-time-txt">{t2}</span></div>
            <div class="r7-item-lista"><span class="r7-tag-jogo r7-volta">VOLTA</span><span class="r7-time-txt">{t2}</span> <span class="r7-vs">X</span> <span class="r7-time-txt">{t1}</span></div>
        </div>
            """
        html_gerado += "</div>"

    html_gerado += """
</div>
<!-- FIM EMBED SORTEIO R7 -->
"""

    st.success("Bloco HTML gerado com sucesso!")
    st.subheader("Copie o código abaixo e cole diretamente no editor HTML da matéria (CMS do R7):")
    st.code(html_gerado, language="html")
