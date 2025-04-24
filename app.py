from flask import Flask, jsonify, request, send_from_directory
import requests
import os

app = Flask(__name__)

# Função que consulta o IBGE pelo CEP
def consulta_ibge_por_cep(cep):
    url = f'https://viacep.com.br/ws/{cep}/json/'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if "erro" not in data:
            return {
                "cep": data.get("cep"),
                "logradouro": data.get("logradouro"),
                "bairro": data.get("bairro"),
                "cidade": data.get("localidade"),
                "estado": data.get("uf"),
                "ibge": data.get("ibge")
            }
    return None

@app.route('/')
def index():
    # Serve o arquivo HTML da página inicial
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/consulta_ibge', methods=['GET'])
def consulta_ibge():
    cep = request.args.get('cep')
    
    if not cep:
        return jsonify({"error": "CEP não informado"}), 400
    
    dados_ibge = consulta_ibge_por_cep(cep)
    
    if dados_ibge:
        return jsonify(dados_ibge)
    else:
        return jsonify({"error": "CEP não encontrado ou inválido"}), 404

if __name__ == '__main__':
    app.run(debug=True)
