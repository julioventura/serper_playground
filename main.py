# pip install requests
# pip install streamlit

import requests
import json
import streamlit as st

# Crie sua API na SERPER gratuita e rapidamente: https://serper.dev/api-key
# SERPER_API_KEY = "cole sua chave aqui"
SERPER_API_KEY = "4439b890022e1f9fe17872ff6f4dfc0470ec83bee"

# Verifica se a chave da API foi definida.
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

        # Salvando os resultados em um arquivo JSON para análise
        with open("search_results.json", "w", encoding="utf-8") as f:
            json.dump(search_results, f, ensure_ascii=False, indent=4)

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

            articles.append({
                "title": title,
                "url": url,
                "snippet": snippet if search_type in ["search", "news", "shopping", "scholar"] else None,
                "thumbnail": thumbnail if search_type in ["search", "images", "videos", "shopping"] else None,
                "richSnippet": richSnippet if search_type == "search" else None,
                "position": position if search_type == "search" else None,
                "source": source if search_type in ["search", "images", "videos", "news", "shopping"] else None,
                "channel": channel if search_type == "videos" else None,
                "duration": duration if search_type == "videos" else None,
                "views": views if search_type == "videos" else None,
                "publication_info": publication_info if search_type == "scholar" else None,
                "cited_by": cited_by if search_type == "scholar" else None,
                "price": price if search_type == "shopping" else None,
                "rating": rating if search_type == "shopping" else None,
                "reviews": reviews if search_type == "shopping" else None,
                "date": date if search_type == "news" else None,
            })
        return articles

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

        print("\nsearch_type = ")
        print(search_type)

        print("\nperiod_choice = ")
        print(period_choice)

        results = search_content(query, search_type, period_choice)

        print("\n\nresults = ")
        print(results)

        st.markdown("\n------------------------\n\n")

        if results:
            for article in results:
                for key, value in article.items():
                    st.write(f"{key.capitalize()}: {value}")
                st.markdown("\n------------------------\n")

if __name__ == "__main__":
    main()


#   "searchParameters": {
#     "q": "apple inc",
#     "type": "places",
#     "tbs": "qdr:h",
#     "engine": "google"
#   },
#   "places": [
#     {
#       "position": 1,
#       "title": "Apple Avalon",
#       "address": "8130 Avalon Blvd, Alpharetta, GA 30009",
#       "latitude": 34.07052,
#       "longitude": -84.27462,
#       "rating": 3.8,
#       "ratingCount": 1400,
#       "category": "Electronics store",
#       "phoneNumber": "(770) 510-1670",
#       "website": "https://www.apple.com/retail/avalon?cid=aos-us-seo-maps",
#       "cid": "136156372451037095"
#     },