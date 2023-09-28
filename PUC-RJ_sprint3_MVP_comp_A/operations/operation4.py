import sqlite3
import os

# Atualizar o valor de uma moeda na carteira
currency_code = input("Digite o código da moeda que deseja atualizar: ")
wallet_db_path = os.path.join(os.getcwd(), "wallet.db")

if os.path.exists(wallet_db_path):
    conn_wallet = sqlite3.connect(wallet_db_path)
    cursor_wallet = conn_wallet.cursor()

    # Verificar se a moeda já existe no banco de dados
    cursor_wallet.execute("SELECT * FROM wallet_currencies WHERE id=?", (currency_code,))
    existing_currency = cursor_wallet.fetchone()

    if existing_currency:
        name, min_size, current_amount = existing_currency[1], existing_currency[2], existing_currency[3]
        print(f"Moeda: {name}, Valor atual: {current_amount}, Valor mínimo: {min_size}")

        while True:
            try:
                new_amount = float(input(f"Digite o novo valor (mínimo {min_size}): "))
                if new_amount >= min_size:
                    # Atualizar o valor da moeda no banco de dados
                    cursor_wallet.execute("UPDATE wallet_currencies SET amount=? WHERE id=?", (new_amount, currency_code))
                    conn_wallet.commit()
                    conn_wallet.close()
                    print(f"Valor de {name} atualizado para {new_amount} na carteira.")
                    break
                else:
                    print("O valor inserido é menor que o tamanho mínimo.")
            except ValueError:
                print("Valor inserido não é um número válido.")
    else:
        conn_wallet.close()
        print("Moeda não consta na carteira, por favor insira uma moeda já existente na carteira.")
else:
    print("A carteira não foi criada. Use a opção 3 para adicionar moedas à carteira primeiro.")
