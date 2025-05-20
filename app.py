from flask import Flask, jsonify
import requests
from models import Country, Session
from models_livraria import Livro, SessionLivraria
from bs4 import BeautifulSoup

app = Flask(__name__)

url = "https://restcountries.com/v3.1"

@app.route('/country/<name>', methods=["GET"])
def get_country(name):
    session = Session()


    existing = session.query(Country).filter(Country.nome_comum.ilike(name)).first()
    if existing:
        return jsonify({
            "nome_comum": existing.nome_comum,
            "nome_oficial": existing.nome_oficial,
            "capital": existing.capital,
            "continente": existing.continente,
            "região": existing.regiao,
            "subregião": existing.subregiao,
            "população": existing.populacao,
            "área": existing.area,
            "moeda": existing.moeda,
            "idioma": existing.idioma,
            "fuso_horário": existing.fuso_horario,
            "bandeira": existing.bandeira_url
        })


    try:
        response = requests.get(f"{url}/name/{name}", timeout=10)
        response.raise_for_status()
        data = response.json()[0]
    except Exception as e:
        return jsonify({"erro": "Erro ao acessar a API externa", "detalhes": str(e)}), 502


    nome_comum = data.get("name", {}).get("common")
    nome_oficial = data.get("name", {}).get("official")
    capital = data.get("capital", [None])[0]
    continente = data.get("continents", [None])[0]
    regiao = data.get("region")
    subregiao = data.get("subregion")
    populacao = data.get("population")
    area = data.get("area")
    

    moedas = data.get("currencies", {})
    moeda = list(moedas.values())[0].get("name") if moedas else None


    idiomas = data.get("languages", {})
    idioma = list(idiomas.values())[0] if idiomas else None

    fuso = data.get("timezones", [None])[0]
    bandeira = data.get("flags", {}).get("png")


    country = Country(
        nome_comum=nome_comum,
        nome_oficial=nome_oficial,
        capital=capital,
        continente=continente,
        regiao=regiao,
        subregiao=subregiao,
        populacao=populacao,
        area=area,
        moeda=moeda,
        idioma=idioma,
        fuso_horario=fuso,
        bandeira_url=bandeira
    )

    session.add(country)
    session.commit()

    return jsonify({
        "nome_comum": nome_comum,
        "nome_oficial": nome_oficial,
        "capital": capital,
        "continente": continente,
        "região": regiao,
        "subregião": subregiao,
        "população": populacao,
        "área": area,
        "moeda": moeda,
        "idioma": idioma,
        "fuso_horário": fuso,
        "bandeira": bandeira
    })





@app.route('/countries', methods=["GET"])
def get_all_countries():
    session = Session()
    countries = session.query(Country).all()

    result = []
    for c in countries:
        result.append({
            "nome_comum": c.nome_comum,
            "nome_oficial": c.nome_oficial,
            "capital": c.capital,
            "continente": c.continente,
            "região": c.regiao,
            "subregião": c.subregiao,
            "população": c.populacao,
            "área": c.area,
            "moeda": c.moeda,
            "idioma": c.idioma,
            "fuso_horário": c.fuso_horario,
            "bandeira": c.bandeira_url
        })

    return jsonify(result)


@app.route('/scrape-livros', methods = ["GET"])
def get_livros():
    url = "https://books.toscrape.com/"
    session = SessionLivraria()
    response = requests.get(url)
    response.encoding = 'utf-8'

    if response.status_code != 200:
        return jsonify({"message": "Erro ao acessar a api"}, response.status_code)
    
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    livros_html = soup.select("article.product_pod")[:10]

    for livro in livros_html:
        titulo = livro.h3.a['title']
        preco = livro.select_one(".price_color").text.replace("£", "").strip()
        avaliacao = livro.select_one(".star-rating")["class"][1]  # Ex: 'Three'
        disponibilidade = livro.select_one(".availability").text.strip()

        novo_livro = Livro(
            titulo=titulo,
            preco=float(preco),
            avaliacao=avaliacao,
            disponibilidade=disponibilidade
        )
        session.add(novo_livro)

    session.commit()

    return jsonify({"mensagem": "10 livros adicionados com sucesso!"})


@app.route('/livros', methods=["GET"])
def listar_livros():
    session = SessionLivraria()
    livros = session.query(Livro).all()

    resultado = []
    for l in livros:
        resultado.append({
            "titulo": l.titulo,
            "preco": l.preco,
            "avaliacao": l.avaliacao,
            "disponibilidade": l.disponibilidade
        })

    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
