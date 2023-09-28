import sqlite3

# Conectar à base de dados do Componente C
conn_original = sqlite3.connect("../PUC-RJ_sprint3_MVP_comp_C/database/db.sqlite3")
cursor_original = conn_original.cursor()

# Consultar a moeda com base no código da base da dados do componente C
currency_code = input("Digite o código da moeda: ")
cursor_original.execute("SELECT name, min_size FROM coinbase_currencies WHERE id=?", (currency_code,))
result = cursor_original.fetchone()
if result:
    name, min_size = result
    print(f"Nome da moeda: {name}")
    print(f"Tamanho mínimo: {min_size}")
else:
    print("Moeda não encontrada.")
