from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask, redirect, request, jsonify
import sqlite3
import os
import subprocess

from flask_cors import CORS


info = Info(title="Componente A: API para interação com a base de dados gerada pelo componente C", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
app_tag = Tag(name="Operações com a Carteira", description="Realizar operações com a Carteira usando o banco de dados do componente C")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

# Conectar com a base de dados wallet
def get_wallet_connection():
    wallet_db_path = os.path.join(os.getcwd(), "wallet.db")
    conn = sqlite3.connect(wallet_db_path)
    return conn

# Rota para listar todas as moedas
@app.get('/1. Listar todas as moedas', methods=['GET'], tags=[app_tag])
def list_currencies():
    conn_original = sqlite3.connect("../PUC-RJ_sprint3_MVP_comp_C/database/db.sqlite3")
    cursor_original = conn_original.cursor()
    cursor_original.execute("SELECT * FROM coinbase_currencies")
    currencies = cursor_original.fetchall()
    conn_original.close()
    if currencies:
        return jsonify(currencies)
    else:
        return "Nenhuma moeda encontrada.", 404

# Rota para pesquisar moeda pelo código
@app.get('/2. Consultar moeda por código', methods=['GET'], tags=[app_tag])
def get_currency():
    
    if request.method == 'GET':
        try:
            subprocess.run(["python", "operations/operation2.py"])
            return "Solicitação para Consultar moeda por código enviada com sucesso", 200
        except Exception as e:
            return f"Erro para Consultar moeda por código: {str(e)}", 500
    else:
        return "Solicitação do método GET necessária.", 400

# Rota para adicionar moedas à carteira (banco de dados wallet.db )
@app.post('/3. Adicionar valor da moeda à carteira', methods=['POST'], tags=[app_tag])
def add_currency_to_wallet():
    
    if request.method == 'POST':
        try:
            subprocess.run(["python", "operations/operation3.py"])
            return "Solicitação para dicionar valor da moeda à carteira enviada com sucesso", 200
        except Exception as e:
            return f"Erro ao Adicionar valor da moeda à carteira: {str(e)}", 500
    else:
        return "Solicitação do método POST necessária.", 400

# Rota para atualizar o valor da moeda no banco de dados wallet.db
@app.put('/4. Atualizar valor de moeda na carteira', methods=['PUT'], tags=[app_tag])
def update_currency_in_wallet():
    
    if request.method == 'PUT':
        try:
            subprocess.run(["python", "operations/operation4.py"])
            return "Solicitação para Atualizar valor de moeda na carteira enviada com sucesso", 200
        except Exception as e:
            return f"Erro ao Atualizar valor de moeda na carteira: {str(e)}", 500
    else:
        return "Solicitação do método POST necessária.", 400

# Rota para deletar a moeda do bancod e dados wallet.db
@app.delete('/5. Remover moeda da carteira', methods=['DELETE'], tags=[app_tag])
def delete_currency_from_wallet():
    
    if request.method == 'DELETE':
        try:
            subprocess.run(["python", "operations/operation5.py"])
            return "Solicitação para Remover moeda da carteira enviada com sucesso", 200
        except Exception as e:
            return f"Erro ao Remover moeda da carteira: {str(e)}", 500
    else:
        return "Solicitação do método POST necessária.", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
