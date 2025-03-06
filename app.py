from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# URL da API de taxas de câmbio
API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

@app.route("/cotacao/<moeda>")
def converter_moeda(moeda):
    try:
        # Fazendo a requisição para a API
        response = requests.get(API_URL)
        
        if response.status_code == 200:
            data = response.json()
            
            # Verificando se a moeda existe nas taxas de câmbio
            if "rates" in data and moeda.upper() in data["rates"] and "BRL" in data["rates"]:
                taxa = data["rates"][moeda.upper()] / data["rates"]["BRL"]
                return jsonify({"moeda": moeda.upper(), "taxa_para_reais": taxa})
            else:
                return jsonify({"erro": "Moeda não encontrada"}), 404
        else:
            return jsonify({"erro": "Falha ao obter dados da API"}), 500
        
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route("/cotacoes")
def todas_cotacoes():
    try:
        response = requests.get(API_URL)
        
        if response.status_code == 200:
            data = response.json()
            
            # Verificando se a API retornou as taxas
            if "rates" in data and "BRL" in data["rates"]:
                taxas_para_reais = {moeda: taxa / data["rates"]["BRL"] for moeda, taxa in data["rates"].items()}
                return jsonify(taxas_para_reais)
            else:
                return jsonify({"erro": "Dados não disponíveis"}), 404
        else:
            return jsonify({"erro": "Falha ao obter dados da API"}), 500
        
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    # Configuração para rodar em produção ou ambiente de desenvolvimento
    port = int(os.environ.get("PORT", 8080))  # Usa a variável de ambiente PORT, ou 8080 se não estiver definida
    app.run(host="0.0.0.0", port=port, debug=True)
