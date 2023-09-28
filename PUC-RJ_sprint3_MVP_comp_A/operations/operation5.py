import sqlite3
import os

# Remover uma moeda da carteira
currency_code = input("Digite o código da moeda que deseja remover: ")
wallet_db_path = os.path.join(os.getcwd(), "wallet.db")

if os.path.exists(wallet_db_path):
    conn_wallet = sqlite3.connect(wallet_db_path)
    cursor_wallet = conn_wallet.cursor()

    # Veriricar se a moeda existe no banco de dados
    cursor_wallet.execute("SELECT * FROM wallet_currencies WHERE id=?", (currency_code,))
    existing_currency = cursor_wallet.fetchone()

    if existing_currency:
        name = existing_currency[1]
        confirmation = input(f"Você realmente deseja remover a moeda {name} da sua carteira? (S/N): ").strip().lower()

        if confirmation == "s":
            # Remover ou não a moeda do banco de dados
            cursor_wallet.execute("DELETE FROM wallet_currencies WHERE id=?", (currency_code,))
            conn_wallet.commit()
            conn_wallet.close()
            print(f"Moeda {name} removida da carteira.")
        elif confirmation == "n":
            conn_wallet.close()
            print(f"Moeda {name} não foi removida da carteira.")
        else:
            conn_wallet.close()
            print("Resposta inválida. A moeda não foi removida da carteira.")
    else:
        conn_wallet.close()
        print("Moeda não consta na carteira, por favor insira uma moeda já existente na carteira.")
else:
    print("A carteira não foi criada. Use a opção 3 para adicionar moedas à carteira primeiro.")
