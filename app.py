import streamlit as st

# Configuração da Página
st.set_page_config(
    page_title="Gerador de Sorteios - R7 Esportes",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ Gerador de Embeds de Sorteios - R7 Esportes")
st.markdown("Ferramenta para a redação gerar os códigos HTML de chaveamentos e potes de forma automatizada.")

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
st.sidebar.info("Preencha os campos ao lado com os nomes dos times separados por vírgula. Ex: `Flamengo (BRA), Palmeiras (BRA)`")

# --- ÁREA PRINCIPAL DE ENTRADA DE DADOS ---
st.header(f"Parâmetros: {campeonato} - {fase}")

dados_input = {}

# Layout de inputs baseado na fase escolhida
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
if st.button("🚀 Gerar Código HTML do Embed", type="primary", use_container_width=True):
    
    # Função auxiliar para formatar strings em listas HTML
    def gerar_itens_html(texto_ virgula):
        itens = [x.strip() for x in texto_virgula.split(",") if x.strip()]
        html_out = ""
        for idx, item in enumerate(itens):
            html_out += f'<div class="item-lista"><span class="pos">{idx+1}</span><span class="time-txt">{item}</span></div>\n'
        return html_out

    # Montagem do HTML autossuficiente (sem precisar de JSON externo)
    titulo_pagina = f"{campeonato} - {fase}"
    
    html_gerado = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo_pagina} - R7 Esportes</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&family=Roboto+Condensed:wght@400;700&display=swap');
        :root {{ --r7-green: #08E148; --gold: #c5a059; --bg-dark: #020a05; }}
        * {{ box-sizing: border-box; }}
        body {{
            background: radial-gradient(circle at center top, #063614 0%, var(--bg-dark) 80%);
            background-attachment: fixed; color: #fff; font-family: 'Roboto Condensed', sans-serif;
            margin: 0; padding: 15px; overflow-x: hidden; 
        }}
        header {{ text-align: center; margin-bottom: 25px; }}
        .logo-header {{ display: flex; align-items: center; justify-content: center; gap: 12px; font-family: 'Oswald', sans-serif; font-size: 2.2rem; text-transform: uppercase; }}
        .logo-r7 {{ background: var(--r7-green); color: #000; padding: 2px 10px; border-radius: 4px; font-weight: 900; }}
        .title-sorteio {{ font-size: 1.6rem; letter-spacing: 1px; color: #fff; font-weight: bold; text-transform: uppercase; font-family: 'Oswald', sans-serif; margin-top: 5px; }}
        .main-wrapper {{ max-width: 1100px; margin: 0 auto; padding-bottom: 30px; }}
        .section-header {{ font-family: 'Oswald', sans-serif; text-transform: uppercase; font-size: 1.3rem; letter-spacing: 2px; margin: 30px 0 15px; text-align: center; padding-bottom: 8px; }}
        .grid-layout {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; }}
        .potes-header {{ color: var(--gold); border-bottom: 2px solid var(--gold); }}
        .grupos-header, .confrontos-header {{ color: var(--r7-green); border-bottom: 2px solid var(--r7-green); }}
        .card {{ background: rgba(0, 0, 0, 0.6); backdrop-filter: blur(10px); border-radius: 6px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.05); height: fit-content; }}
        .card-header {{ font-family: 'Oswald', sans-serif; text-align: center; padding: 10px; font-weight: bold; text-transform: uppercase; font-size: 1.1rem; }}
        .item-lista {{ display: flex; align-items: center; padding: 12px 15px; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.95rem; }}
        .item-lista:last-child {{ border: none; }}
        .pos {{ width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; border-radius: 50%; font-size: 0.8rem; margin-right: 12px; font-weight: bold; }}
        .time-txt {{ font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; }}
        
        /* Estilos específicos */
        .card.pote {{ border: 1px solid rgba(197, 160, 89, 0.3); }}
        .card.pote .card-header {{ background: linear-gradient(to right, #6e5221, #c5a059, #6e5221); color: #000; }}
        .card.pote .pos {{ background: rgba(197, 160, 89, 0.15); color: var(--gold); border: 1px solid var(--gold); }}

        .card.grupo, .card.confronto {{ border: 1px solid rgba(8, 225, 72, 0.4); }}
        .card.grupo .card-header, .card.confronto .card-header {{ background: linear-gradient(to right, #031a0b, #0a4d20, #031a0b); color: var(--r7-green); border-bottom: 2px solid var(--r7-green); }}
        .card.grupo .pos, .card.confronto .pos {{ background: rgba(8, 225, 72, 0.2); color: var(--r7-green); border: 1px solid var(--r7-green); }}
        
        .tag-jogo {{ font-size: 0.65rem; padding: 2px 5px; border-radius: 3px; margin-right: 10px; font-weight: bold; min-width: 42px; text-align: center; }}
        .ida {{ background: var(--r7-green); color: #000; }}
        .volta {{ background: #fff; color: #000; }}
        .vs {{ margin: 0 8px; color: var(--r7-green); font-style: italic; font-size: 0.8rem; font-weight: bold; }}
        
        @media (max-width: 768px) {{ .grid-layout {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="main-wrapper" id="content-height-wrapper">
        <header>
            <div class="logo-header"><span class="logo-r7">R7</span> ESPORTES</div>
            <div class="title-sorteio">{titulo_pagina}</div>
        </header>
"""

    # Gerando o conteúdo interno de acordo com a fase selecionada
    if "Fase de Grupos" in fase:
        html_gerado += f"""
        <div class="section-header potes-header">Potes do Sorteio</div>
        <div class="grid-layout">
            <div class="card pote"><div class="card-header">Pote 1</div>{gerar_itens_html(dados_input["pote1"])}</div>
            <div class="card pote"><div class="card-header">Pote 2</div>{gerar_itens_html(dados_input["pote2"])}</div>
            <div class="card pote"><div class="card-header">Pote 3</div>{gerar_itens_html(dados_input["pote3"])}</div>
            <div class="card pote"><div class="card-header">Pote 4</div>{gerar_itens_html(dados_input["pote4"])}</div>
        </div>

        <div class="section-header grupos-header">Grupos da Competição</div>
        <div class="grid-layout">
            <div class="card grupo"><div class="card-header">Grupo A</div>{gerar_itens_html(dados_input["grupoA"])}</div>
            <div class="card grupo"><div class="card-header">Grupo B</div>{gerar_itens_html(dados_input["grupoB"])}</div>
            <div class="card grupo"><div class="card-header">Grupo C</div>{gerar_itens_html(dados_input["grupoC"])}</div>
            <div class="card grupo"><div class="card-header">Grupo D</div>{gerar_itens_html(dados_input["grupoD"])}</div>
            <div class="card grupo"><div class="card-header">Grupo E</div>{gerar_itens_html(dados_input["grupoE"])}</div>
            <div class="card grupo"><div class="card-header">Grupo F</div>{gerar_itens_html(dados_input["grupoF"])}</div>
            <div class="card grupo"><div class="card-header">Grupo G</div>{gerar_itens_html(dados_input["grupoG"])}</div>
            <div class="card grupo"><div class="card-header">Grupo H</div>{gerar_itens_html(dados_input["grupoH"])}</div>
        </div>
        """
    else: # Oitavas ou Quartas
        pote_unico_itens = [x.strip() for x in dados_input["poteUnico"].split(",") if x.strip()]
        html_pote_grid = "".join([f'<div style="background: rgba(197, 160, 89, 0.1); border: 1px solid rgba(197, 160, 89, 0.3); padding: 8px; border-radius: 4px; text-align: center; font-weight: bold; text-transform: uppercase; font-size: 0.9rem;">{t}</div>' for t in pote_unico_itens])
        
        html_gerado += f"""
        <div class="section-header potes-header">Equipes Classificadas (Pote Único)</div>
        <div class="card pote" style="margin-bottom: 30px;">
            <div class="card-header">Pote Único</div>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; padding: 15px;">
                {html_pote_grid}
            </div>
        </div>

        <div class="section-header confrontos-header">Confrontos Definidos</div>
        <div class="grid-layout">
        """
        
        for idx, chave_str in enumerate(dados_input["chaves"]):
            partes = [p.strip() for p in chave_str.split(",")]
            t1 = partes[0] if len(partes) > 0 else "Time A"
            t2 = partes[1] if len(partes) > 1 else "Time B"
            
            html_gerado += f"""
            <div class="card confronto">
                <div class="card-header">Confronto {idx+1}</div>
                <div class="item-lista"><span class="tag-jogo ida">IDA</span><span class="time-txt">{t1}</span> <span class="vs">X</span> <span class="time-txt">{t2}</span></div>
                <div class="item-lista"><span class="tag-jogo volta">VOLTA</span><span class="time-txt">{t2}</span> <span class="vs">X</span> <span class="time-txt">{t1}</span></div>
            </div>
            """
        html_gerado += "</div>"

    # Rodapé do HTML do embed com o script de redimensionamento automatizado
    html_gerado += """
    </div>
    <script>
        function notifyHeight() {
            const wrapper = document.getElementById('content-height-wrapper');
            if(wrapper) {
                const height = Math.ceil(wrapper.getBoundingClientRect().height);
                window.parent.postMessage({ sentinel: 'amp', type: 'embed-size', height: height + 20 }, '*');
            }
        }
        window.addEventListener('load', notifyHeight);
        window.addEventListener('resize', notifyHeight);
    </script>
</body>
</html>
"""

    st.success("Código gerado com sucesso!")
    st.subheader("Copie o código abaixo e salve no seu servidor estático para gerar o embed:")
    st.code(html_gerado, language="html")
