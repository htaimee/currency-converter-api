from flask import Flask, jsonify
import requests

app = Flask(__name__)

# URL de uma API pública para obter taxas de câmbio
API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

@app.route("/cotacao/<moeda>")
def converter_moeda(moeda):
    try:
        response = requests.get(API_URL)
        data = response.json()
        
        if "rates" in data and moeda.upper() in data["rates"] and "BRL" in data["rates"]:
            taxa = data["rates"][moeda.upper()] / data["rates"]["BRL"]
            return jsonify({"moeda": moeda.upper(), "taxa_para_reais": taxa})
        else:
            return jsonify({"erro": "Moeda não encontrada"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route("/cotacoes")
def todas_cotacoes():
    try:
        response = requests.get(API_URL)
        data = response.json()
        
        if "rates" in data and "BRL" in data["rates"]:
            taxas_para_reais = {moeda: taxa / data["rates"]["BRL"] for moeda, taxa in data["rates"].items()}
            return jsonify(taxas_para_reais)
        else:
            return jsonify({"erro": "Dados não disponíveis"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
commit
