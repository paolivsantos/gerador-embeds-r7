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
    [
        "CONMEBOL Libertadores",
        "Copa do Brasil",
        "Copa Sul-Americana",
        "Campeonato Paulista",
        "Copa São Paulo de Futebol Júnior"
    ]
)

if campeonato == "Campeonato Paulista":
    fase = st.sidebar.selectbox(
        "Selecione a Fase",
        ["Fase de Grupos (4 Potes e 4 Grupos)"]
    )
elif campeonato == "Copa São Paulo de Futebol Júnior":
    fase = st.sidebar.selectbox(
        "Selecione a Fase",
        [
            "Fase de Grupos (Grupos 1 ao 32)",
            "Oitavas de Final (Jogo Único)",
            "Quartas de Final (Jogo Único)",
            "Semifinais (Jogo Único)",
            "Final (Jogo Único)"
        ]
    )
else:
    fase = st.sidebar.selectbox(
        "Selecione a Fase",
        [
            "Fase de Grupos (Potes e Grupos)",
            "Oitavas de Final (Pote Único)",
            "Quartas de Final (Pote Único)",
            "Semifinais (Confrontos)"
        ]
    )

st.sidebar.markdown("---")
st.sidebar.info("Preencha os campos ao lado com os nomes dos times separados por vírgula. Ex: `São Paulo Sub-20, Palmeiras Sub-20`")

# --- ÁREA PRINCIPAL DE ENTRADA DE DADOS ---
st.header(f"Parâmetros: {campeonato} - {fase}")

dados_input = {}

# ==========================================
# 1. COPA SÃO PAULO DE FUTEBOL JÚNIOR
# ==========================================
if campeonato == "Copa São Paulo de Futebol Júnior" and "Fase de Grupos" in fase:
    st.subheader("Grupos da Copinha (1 ao 32)")
    st.caption("Preencha os times de cada grupo separados por vírgula. Grupos deixados em branco não aparecerão no HTML final (ou você pode preencher todos os 32).")

    exemplos_copinha = {
        1: "Mirassol, Criciúma, Chapecoense, União Suzano",
        2: "Tanabi, Athletico-PR, Goiás, Santa Cruz",
        3: "Votuporanguense, Botafogo, Floresta, Fast Clube",
        4: "Atlético Guaratinguetá, Grêmio, Porto Vitória, Nova Iguaçu",
        5: "América-SP, Palmeiras, Remo, Olímpia",
        6: "Comercial, Sport, Cascavel, Galvez",
        7: "Bandeirante, Cruzeiro, Capivariano, Real Brasília",
        8: "Ferroviária, Vitória, São José-RS, Serra Branca",
        9: "Ituano, Corinthians, Rio Branco-AC, Santo André",
        10: "Desportivo Brasil, Cuiabá, Ponte Preta, Dom Bosco",
        11: "União Barbarense, Bahia, Coritiba, Madureira",
        12: "EC São Bernardo, Internacional, América-RN, Portuguesa Santista",
        13: "Taubaté, Fluminense, Goiás/Seleção, Água Santa",
        14: "Atlético Mogi, Fortaleza, São Bento, Imperatriz",
        15: "São Carlos, Vasco, XV de Piracicaba, Falcon",
        16: "Ibrachina, Atlético-MG, Portuguesa, Monteiro",
        17: "Guarani, Botafogo-SP, Sampaio Corrêa, Tiradentes",
        18: "Nacional-SP, Santos, Joinville, Tirol",
        19: "Flamengo de Guarulhos, Juventude, Operário-PR, Boavista",
        20: "Jabaquara, Red Bull Bragantino, Náutico, Sparta",
        21: "Audax-SP, São Paulo, Vila Nova, Operário-MS",
        22: "Santo André/Mauá, Ceará, Athletico/Paraná, Capital",
        23: "Água Santa/Diadema, Avaí, Londrina, Pinheiros",
        24: "Oeste, Botafogo/RJ, Tuna Luso, Rio Branco-ES",
        25: "Noroeste, Corinthians/Paulista, ABC, Vocem",
        26: "Marília, Grêmio/RS, Confiança, América-MG",
        27: "Penapolense, Palmeiras/SP, Ypiranga-RS, Barra-SC",
        28: "Rio Claro, Santos/SP, CSA, Hercílio Luz",
        29: "Sertãozinho, São Paulo/SP, CRB, Maranhão",
        30: "Lemense, Flamengo, Nova Venécia, Zumbi",
        31: "Monte Azul, Cruzeiro/MG, Paysandu, Pinheiro",
        32: "Francana, Botafogo, Retrô, Ceilândia"
    }

    dados_input["grupos_copinha"] = {}
    cols_copinha = st.columns(4)
    for g in range(1, 33):
        col_atual = cols_copinha[(g - 1) % 4]
        with col_atual:
            valor_padrao = exemplos_copinha.get(g, f"Time {g}A, Time {g}B, Time {g}C, Time {g}D")
            dados_input["grupos_copinha"][g] = st.text_input(f"Grupo {g:02d}", valor_padrao, key=f"copinha_g_{g}")

elif campeonato == "Copa São Paulo de Futebol Júnior" and "Jogo Único" in fase:
    qtd_confrontos_map = {
        "Oitavas de Final (Jogo Único)": 8,
        "Quartas de Final (Jogo Único)": 4,
        "Semifinais (Jogo Único)": 2,
        "Final (Jogo Único)": 1
    }
    qtd = qtd_confrontos_map[fase]
    st.subheader(f"Confrontos - {fase}")
    chaves_cols = st.columns(2 if qtd > 1 else 1)
    dados_input["chaves_jogo_unico"] = []
    for i in range(1, qtd + 1):
        with chaves_cols[(i - 1) % len(chaves_cols)]:
            label_confronto = "Grande Final" if qtd == 1 else f"Confronto {i}"
            val = st.text_input(f"{label_confronto} (Ex: Time A, Time B)", f"Time A{i}, Time B{i}", key=f"copinha_ju_{i}")
            dados_input["chaves_jogo_unico"].append((label_confronto, val))

# ==========================================
# 2. CAMPEONATO PAULISTA
# ==========================================
elif campeonato == "Campeonato Paulista" and "Fase de Grupos" in fase:
    st.subheader("1. Potes do Paulistão (Potes 1 a 4)")
    col1, col2 = st.columns(2)
    with col1:
        dados_input["pote1"] = st.text_area("Pote 1 (Sep. por vírgula)", "Palmeiras, São Paulo, Corinthians, Santos")
        dados_input["pote2"] = st.text_area("Pote 2 (Sep. por vírgula)", "Red Bull Bragantino, Novorizontino, Internacional de Limeira, Mirassol")
    with col2:
        dados_input["pote3"] = st.text_area("Pote 3 (Sep. por vírgula)", "Água Santa, Santo André, Portuguesa, Guarani")
        dados_input["pote4"] = st.text_area("Pote 4 (Sep. por vírgula)", "Ponte Preta, Novorizontino, Botafogo-SP, Velo Clube")

    st.subheader("2. Grupos de Destino (A ao D)")
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        dados_input["grupoA"] = st.text_input("Grupo A", "Palmeiras, Internacional de Limeira, Botafogo-SP, Portuguesa")
        dados_input["grupoB"] = st.text_input("Grupo B", "Santos, Red Bull Bragantino, Guarani, Velo Clube")
    with g_col2:
        dados_input["grupoC"] = st.text_input("Grupo C", "São Paulo, Mirassol, Água Santa, Ponte Preta")
        dados_input["grupoD"] = st.text_input("Grupo D", "Corinthians, Novorizontino, Santo André, (Time A)")

# ==========================================
# 3. LIBERTADORES / SUL-AMERICANA / COPA DO BRASIL
# ==========================================
elif "Fase de Grupos" in fase:
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
        with chaves_cols[(i - 1) % 2]:
            val = st.text_input(f"Confronto {i} (Ex: Time A, Time B)", f"Time A{i}, Time B{i}")
            dados_input["chaves"].append(val)

elif "Quartas de Final" in fase:
    dados_input["poteUnico"] = st.text_area("Times Classificados (Pote Único)", "Palmeiras, Santos, Vasco, Atlético-MG, Cruzeiro, Grêmio, Internacional, Vitória")
    st.subheader("Confrontos (Ida e Volta)")
    chaves_cols = st.columns(2)
    dados_input["chaves"] = []
    for i in range(1, 5):
        with chaves_cols[(i - 1) % 2]:
            val = st.text_input(f"Confronto {i} (Ex: Time A, Time B)", f"Time A{i}, Time B{i}")
            dados_input["chaves"].append(val)

elif "Semifinais" in fase:
    dados_input["poteUnico"] = st.text_area("Times Classificados para as Semis", "Flamengo, Palmeiras, Corinthians, São Paulo")
    st.subheader("Confrontos das Semifinais (Ida e Volta)")
    chaves_cols = st.columns(2)
    dados_input["chaves"] = []
    for i in range(1, 3):
        with chaves_cols[(i - 1) % 2]:
            val = st.text_input(f"Chave {i} (Ex: Time A, Time B)", f"Time A{i}, Time B{i}")
            dados_input["chaves"].append(val)

# --- BOTÃO DE GERAÇÃO DO CÓDIGO ---
st.markdown("---")
if st.button("🚀 Gerar Bloco HTML para o CMS", type="primary", use_container_width=True):

    def gerar_itens_html(texto_virgula):
        itens = [x.strip() for x in texto_virgula.split(",") if x.strip()]
        html_out = ""
        for idx, item in enumerate(itens):
            html_out += f'<div class="r7-item-lista"><span class="r7-pos">{idx + 1}</span><span class="r7-time-txt">{item}</span></div>\n'
        return html_out

    titulo_campeonato = campeonato
    subtitulo_fase = fase

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
    #r7-sorteio-wrapper .r7-title-sorteio {{
        font-size: 1.45rem;
        letter-spacing: 0.8px;
        color: #fff;
        font-weight: 700;
        text-transform: uppercase;
        font-family: 'Oswald', sans-serif;
        margin-top: 8px;
        line-height: 1.2;
        text-wrap: balance;
    }}
    #r7-sorteio-wrapper .r7-subtitle-fase {{
        display: block;
        font-size: 0.95rem;
        letter-spacing: 1.4px;
        color: #c5a059;
        font-weight: 700;
        text-transform: uppercase;
        font-family: 'Roboto Condensed', sans-serif;
        margin-top: 6px;
        line-height: 1.3;
        text-wrap: balance;
    }}
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

    #r7-sorteio-wrapper .r7-tag-jogo {{ font-size: 0.6rem; padding: 2px 4px; border-radius: 3px; margin-right: 8px; font-weight: bold; min-width: 44px; text-align: center; }}
    #r7-sorteio-wrapper .r7-ida, #r7-sorteio-wrapper .r7-unico {{ background: #08E148; color: #000; }}
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
        <div class="r7-title-sorteio">{titulo_campeonato}</div>
        <div class="r7-subtitle-fase">{subtitulo_fase}</div>
    </header>
"""

    if campeonato == "Copa São Paulo de Futebol Júnior" and "Fase de Grupos" in fase:
        cards_grupos = ""
        for g, texto_times in dados_input["grupos_copinha"].items():
            if texto_times.strip():
                cards_grupos += f'        <div class="r7-card r7-grupo"><div class="r7-card-header">Grupo {g:02d}</div>{gerar_itens_html(texto_times)}</div>\n'

        html_gerado += f"""
    <div class="r7-section-header r7-grupos-header">Grupos da Copinha</div>
    <div class="r7-grid-layout">
{cards_grupos}    </div>
"""

    elif campeonato == "Copa São Paulo de Futebol Júnior" and "Jogo Único" in fase:
        html_gerado += """
    <div class="r7-section-header r7-confrontos-header">Confrontos (Jogo Único)</div>
    <div class="r7-grid-layout">
"""
        for label_confronto, chave_str in dados_input["chaves_jogo_unico"]:
            partes = [p.strip() for p in chave_str.split(",")]
            t1 = partes[0] if len(partes) > 0 and partes[0] else "Time A"
            t2 = partes[1] if len(partes) > 1 and partes[1] else "Time B"

            html_gerado += f"""
        <div class="r7-card r7-confronto">
            <div class="r7-card-header">{label_confronto}</div>
            <div class="r7-item-lista"><span class="r7-tag-jogo r7-unico">ÚNICO</span><span class="r7-time-txt">{t1}</span> <span class="r7-vs">X</span> <span class="r7-time-txt">{t2}</span></div>
        </div>
"""
        html_gerado += "    </div>\n"

    elif campeonato == "Campeonato Paulista":
        html_gerado += f"""
    <div class="r7-section-header r7-potes-header">Potes do Sorteio</div>
    <div class="r7-grid-layout">
        <div class="r7-card r7-pote"><div class="r7-card-header">Pote 1</div>{gerar_itens_html(dados_input["pote1"])}</div>
        <div class="r7-card r7-pote"><div class="r7-card-header">Pote 2</div>{gerar_itens_html(dados_input["pote2"])}</div>
        <div class="r7-card r7-pote"><div class="r7-card-header">Pote 3</div>{gerar_itens_html(dados_input["pote3"])}</div>
        <div class="r7-card r7-pote"><div class="r7-card-header">Pote 4</div>{gerar_itens_html(dados_input["pote4"])}</div>
    </div>

    <div class="r7-section-header r7-grupos-header">Grupos do Paulistão</div>
    <div class="r7-grid-layout">
        <div class="r7-card r7-grupo"><div class="r7-card-header">Grupo A</div>{gerar_itens_html(dados_input["grupoA"])}</div>
        <div class="r7-card r7-grupo"><div class="r7-card-header">Grupo B</div>{gerar_itens_html(dados_input["grupoB"])}</div>
        <div class="r7-card r7-grupo"><div class="r7-card-header">Grupo C</div>{gerar_itens_html(dados_input["grupoC"])}</div>
        <div class="r7-card r7-grupo"><div class="r7-card-header">Grupo D</div>{gerar_itens_html(dados_input["grupoD"])}</div>
    </div>
"""

    elif "Fase de Grupos" in fase:
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
        cols_grid = 4 if len(pote_unico_itens) > 2 else 2
        html_pote_grid = "".join([
            f'<div style="background: rgba(197, 160, 89, 0.1); border: 1px solid rgba(197, 160, 89, 0.3); padding: 8px; border-radius: 4px; text-align: center; font-weight: bold; text-transform: uppercase; font-size: 0.85rem;">{t}</div>'
            for t in pote_unico_itens
        ])

        titulo_bloco_pote = "Classificados" if "Semifinais" in fase else "Equipes Classificadas (Pote Único)"

        html_gerado += f"""
    <div class="r7-section-header r7-potes-header">{titulo_bloco_pote}</div>
    <div class="r7-card r7-pote" style="margin-bottom: 25px;">
        <div class="r7-card-header">Participantes</div>
        <div class="r7-pote-times-grid" style="display: grid; grid-template-columns: repeat({cols_grid}, 1fr); gap: 8px; padding: 12px;">
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
            <div class="r7-card-header">Chave {idx + 1}</div>
            <div class="r7-item-lista"><span class="r7-tag-jogo r7-ida">IDA</span><span class="r7-time-txt">{t1}</span> <span class="r7-vs">X</span> <span class="r7-time-txt">{t2}</span></div>
            <div class="r7-item-lista"><span class="r7-tag-jogo r7-volta">VOLTA</span><span class="r7-time-txt">{t2}</span> <span class="r7-vs">X</span> <span class="r7-time-txt">{t1}</span></div>
        </div>
"""
        html_gerado += "    </div>\n"

    html_gerado += """
</div>
<!-- FIM EMBED SORTEIO R7 -->
"""

    st.success("Bloco HTML gerado com sucesso!")
    st.subheader("Copie o código abaixo e cole diretamente no editor HTML da matéria (CMS do R7):")
    st.code(html_gerado, language="html")
