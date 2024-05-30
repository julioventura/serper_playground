# pip install requests
# pip install streamlit

import requests
import json
import streamlit as st


# Definir a variável path_result no início do script (apenas o caminho)
path_results = "./results/"

# Crie sua API na SERPER gratuita e rapidamente: https://serper.dev/api-key
SERPER_API_KEY = "cole sua chave aqui"

if not SERPER_API_KEY or SERPER_API_KEY == "cole sua chave aqui":
    serper_api_key = SERPER_API_KEY

    if 'serper_api_key' not in st.session_state:
        st.session_state['serper_api_key'] = ''

    # Placeholder para o campo de input
    input_placeholder = st.empty()

    # Mostrar o campo de input se a chave não foi preenchida
    if st.session_state['serper_api_key'] == '':
        with input_placeholder.container():
            serper_api_key = st.text_input("Sua CHAVE API SERPER (https://serper.dev/api-key)", key="serper_api_key_1")
            # if st.button('Confirmar'):
            if serper_api_key:
                st.session_state['serper_api_key'] = serper_api_key
                input_placeholder.empty()

    # Utilizando as chaves API inseridas
    if st.session_state['serper_api_key']:
        SERPER_API_KEY = st.session_state['serper_api_key']
    
    # Verificação final de se a chave da API foi definida.
    if not SERPER_API_KEY or SERPER_API_KEY == "cole sua chave aqui":
        st.error("\nERRO: \nVocê precisa fornecer uma chave de API do Serper. \nCrie uma gratuitamente em https://serper.dev/api-key\n\n")
        st.stop()  # Encerra o programa se não houver chave.


# Busca de conteúdo na web
def search_content(query, search_type="search", period_choice="y"):
    headers = {
        "X-API-KEY": SERPER_API_KEY
    }

    # Função para obter a string do parâmetro 'tbs' com base na escolha do usuário.
    def get_tbs_param(choice):
        tbs_options = {
            "Última hora": "qdr:h",
            "Últimas 24 horas (dia)": "qdr:d",
            "Última semana": "qdr:w",
            "Último mês": "qdr:m",
            "Último ano": "qdr:y",
            "Qualquer data": ""
        }
        return tbs_options.get(choice, "")  # Retorna vazio se a escolha for inválida

    tbs_param = get_tbs_param(period_choice)

    params = {
        "q": query,
        "gl": "br",  # país
        "hl": "pt-br",  # linguagem
        "type": search_type,  # search / images / videos / news / shopping / scholar / autocomplete / webpage
        "tbs": tbs_param,  # Parâmetro de período definido aqui (h, d, w, m, y, None).
        "engine": "google"
    }
    # "tbs": f"{tbs_param}" if tbs_param else "",  # Parâmetro de período definido aqui.

    # Verifique se o tbs está sendo formatado corretamente para diferentes períodos:
    if period_choice == "Última hora":
        assert params["tbs"] == "qdr:h"
    elif period_choice == "Últimas 24 horas (dia)":
        assert params["tbs"] == "qdr:d"
    elif period_choice == "Última semana":
        assert params["tbs"] == "qdr:w"
    elif period_choice == "Último mês":
        assert params["tbs"] == "qdr:m"
    elif period_choice == "Último ano":
        assert params["tbs"] == "qdr:y"
    elif period_choice == "Qualquer data":
        assert params["tbs"] == ""
    else:
        raise ValueError(f"Período inválido: {period_choice}")

    try:
        st.write(f"Enviando requisição para a API do Serper com a query: {query} e tipo de busca: {search_type}")
        response = requests.get("https://google.serper.dev/search", headers=headers, params=params)
        st.write(f"Código de status da resposta: {response.status_code}")
        response.raise_for_status()

        search_results = response.json()

        
        # Salvando os resultados em um arquivo JSON para análise em path_results
        # Nome do arquivo
        file_name = "search_results.json"
        full_path = path_results + file_name

        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(search_results, f, ensure_ascii=False, indent=4)
            st.write(f"Resultados salvos em: {full_path}")

        # Verificando se a chave 'organic' existe nos resultados
        if 'organic' not in search_results:
            st.write("\nA chave 'organic' não foi encontrada nos resultados da busca. \nResultados completos:\n")
        st.write("\nsearch_results")
        st.write(search_results)

        articles = []
        for i, result in enumerate(search_results.get(search_type + "_results", [])):
            st.markdown(f"\n--- Resultado da Busca ({search_type}) - {i+1} ---")

            if search_type == "search":
                title = result.get('title')
                url = result.get('link')
                snippet = result.get('snippet')
                thumbnail = result.get('thumbnail')
                richSnippet = result.get('rich_snippet', {})
                position = result.get('position')
                source = result.get('source')

                st.write(f"Título: {title}")
                st.write(f"URL: {url}")
                st.write(f"Snippet: {snippet}")
                if thumbnail:
                    st.write(f"Thumbnail: {thumbnail}")
                if richSnippet:
                    st.write(f"Rich Snippet:")
                    for key, value in richSnippet.items():
                        st.write(f"  {key}: {json.dumps(value, indent=2)}")
                st.write(f"Posição: {position}")
                st.write(f"Fonte: {source}")

            elif search_type == "images":
                title = result.get('title')
                url = result.get('link')
                thumbnail = result.get('thumbnail')
                source = result.get('source')

                st.write(f"Título: {title}")
                st.write(f"URL: {url}")
                st.write(f"Thumbnail: {thumbnail}")
                st.write(f"Fonte: {source}")

            elif search_type == "videos":
                title = result.get('title')
                url = result.get('link')
                thumbnail = result.get('thumbnail')
                channel = result.get('channel')
                duration = result.get('duration')
                views = result.get('views')

                st.write(f"Título: {title}")
                st.write(f"URL: {url}")
                st.write(f"Thumbnail: {thumbnail}")
                st.write(f"Canal: {channel}")
                st.write(f"Duração: {duration}")
                st.write(f"Visualizações: {views}")

            elif search_type == "news":
                title = result.get('title')
                url = result.get('link')
                snippet = result.get('snippet')
                publication = result.get('publication', {})
                source = publication.get('name')
                date = publication.get('date')

                st.write(f"Título: {title}")
                st.write(f"URL: {url}")
                st.write(f"Snippet: {snippet}")
                if source:
                    st.write(f"Fonte: {source}")
                if date:
                    st.write(f"Data: {date}")

            elif search_type == "shopping":
                title = result.get('title')
                url = result.get('link')
                snippet = result.get('snippet')
                price = result.get('price')
                rating = result.get('rating')
                reviews = result.get('reviews')
                source = result.get('source')
                thumbnail = result.get('thumbnail')

                st.write(f"Título: {title}")
                st.write(f"URL: {url}")
                st.write(f"Snippet: {snippet}")
                if price:
                    st.write(f"Preço: {price}")
                if rating:
                    st.write(f"Avaliação: {rating}")
                if reviews:
                    st.write(f"Avaliações: {reviews}")
                st.write(f"Fonte: {source}")
                if thumbnail:
                    st.write(f"Thumbnail: {thumbnail}")

            elif search_type == "scholar":
                title = result.get('title')
                url = result.get('link')
                snippet = result.get('snippet')
                publication_info = result.get('publication_info', {})
                cited_by = result.get('cited_by', {})

                st.write(f"Título: {title}")
                st.write(f"URL: {url}")
                st.write(f"Snippet: {snippet}")
                if publication_info:
                    st.write("Informações da Publicação:")
                    for key, value in publication_info.items():
                        st.write(f"  {key}: {value}")
                if cited_by:
                    st.write(f"Citado por: {cited_by}")

    except requests.exceptions.HTTPError as errh:
        st.error(f"Erro HTTP: {errh}")
        if errh.response.status_code == 404:
            st.error("Endpoint da API não encontrado. Verifique a documentação do Serper.")
    except requests.exceptions.RequestException as err:
        st.error(f"Erro na Solicitação: {err}")
    except Exception as e:
        st.error(f"Erro Inesperado: {e}")

    return []

# Função para selecionar o tipo de busca
def choose_search_type():
    st.markdown("#### Tipo de busca:")
    choice = st.radio(
        "",
        [
            "Busca comum do Google",
            "Imagens",
            "Videos",
            "Notícias",
            "Shopping",
            "Scholar (artigos acadêmicos)",
        ],
        horizontal=False
    )
    search_types = {
        "Busca comum do Google": "search",
        "Imagens": "images",
        "Videos": "videos",
        "Notícias": "news",
        "Shopping": "shopping",
        "Scholar (artigos acadêmicos)": "scholar",
    }
    return search_types.get(choice, "search")


# Função principal para executar todas as etapas
def main():
    st.title("Pesquisa com Serper")

    st.markdown("#### Período da busca:")
    period_choice = st.radio(
        "",
        [
            "Última hora",
            "Últimas 24 horas (dia)",
            "Última semana",
            "Último mês",
            "Último ano",
            "Qualquer data",
        ],
        horizontal=False
    )

    search_type = choose_search_type()

    st.markdown("#### Buscar por:")
    query = st.text_input("")
    
    if st.button("Buscar"):
        print("\n\n\n")
        print("query = " + query)                           # Usando concatenação de strings
        print(f"search_type = {search_type}")               # Usando f-string (recomendado)
        print("period_choice = {}".format(period_choice))   # Usando str.format()

        results = search_content(query, search_type, period_choice)

        st.markdown("\n------------------------\n\n")

if __name__ == "__main__":
    main()

