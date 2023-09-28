import sqlite3
import os

# Conectar à base de dados do Componente C
conn_original = sqlite3.connect("../PUC-RJ_sprint3_MVP_comp_C/database/db.sqlite3")
cursor_original = conn_original.cursor()

# Adicionar uma moeda à carteira respeitando o valor mínimo
currency_code = input("Qual moeda adicionar à carteira (código): ")
cursor_original.execute("SELECT name, min_size FROM coinbase_currencies WHERE id=?", (currency_code,))
result = cursor_original.fetchone()

if result:
    name, min_size = result
    while True:
        try:
            amount = float(input(f"Digite o valor (mínimo {min_size}): "))
            if amount >= min_size:
                # Criar nova base de dados (wallet.db) com o valor da moeda inserido (coluna "amount")
                wallet_db_path = os.path.join(os.getcwd(), "wallet.db")
                conn_wallet = sqlite3.connect(wallet_db_path)
                cursor_wallet = conn_wallet.cursor()

                # Create the wallet_currencies table if it doesn't exist
                cursor_wallet.execute("""
                    CREATE TABLE IF NOT EXISTS wallet_currencies (
                        id TEXT PRIMARY KEY,
                        name TEXT,
                        min_size REAL,
                        amount REAL
                    )
                """)

                # Verificar se a moeda já existe no banco de dados
                cursor_wallet.execute("SELECT * FROM wallet_currencies WHERE id=?", (currency_code,))
                existing_currency = cursor_wallet.fetchone()

                if existing_currency:
                    # Se a moeda existir, adicione ao valor
                    current_amount = existing_currency[3]
                    new_amount = current_amount + amount
                    cursor_wallet.execute("UPDATE wallet_currencies SET amount=? WHERE id=?", (new_amount, currency_code))
                else:
                    # Se a moeda não existir, insira no banco de dados
                    cursor_wallet.execute("""
                        INSERT INTO wallet_currencies (id, name, min_size, amount) VALUES (?, ?, ?, ?)
                    """, (currency_code, name, min_size, amount))

                conn_wallet.commit()
                conn_wallet.close()
                print(f"Adicionado {amount} {currency_code} à carteira.")
                break
            else:
                print("O valor inserido é menor que o tamanho mínimo.")
        except ValueError:
            print("Valor inserido não é um número válido.")
else:
    print("Moeda não encontrada.")
