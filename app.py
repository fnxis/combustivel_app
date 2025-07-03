from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

DB = 'abastecimentos.db'

def get_db_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# Criação da tabela com colunas adicionais
def criar_tabela():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Cria a tabela se não existir
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS abastecimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            litros REAL,
            valor REAL,
            km REAL
        )
    """)

    # Verifica se as colunas extras existem, senão adiciona
    colunas_necessarias = {
        "km_restante": "REAL",
        "litros_restantes": "REAL"
    }

    # Consulta os nomes das colunas existentes na tabela
    cursor.execute("PRAGMA table_info(abastecimentos)")
    colunas_existentes = [col[1] for col in cursor.fetchall()]

    for coluna, tipo in colunas_necessarias.items():
        if coluna not in colunas_existentes:
            cursor.execute(f"ALTER TABLE abastecimentos ADD COLUMN {coluna} {tipo}")
            print(f"Coluna '{coluna}' adicionada à tabela.")

    conn.commit()
    conn.close()
    
criar_tabela()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            litros = float(request.form["litros"])
            valor = float(request.form["valor"])
            km = float(request.form["km"])
            data = datetime.now().strftime("%d/%m/%Y %H:%M")

            # Cálculo
            km_total = litros * 10
            km_restante = max(0, km_total - km)
            litros_restantes = max(0, km_restante / 10)

            conn = get_db_connection()
            conn.execute("""
                INSERT INTO abastecimentos (data, litros, valor, km, km_restante, litros_restantes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (data, litros, valor, km, km_restante, litros_restantes))
            conn.commit()
            conn.close()

            flash("Abastecimento salvo com sucesso!", "success")
            return redirect(url_for("index"))

        except ValueError:
            flash("Preencha todos os campos com números válidos.", "danger")
            return redirect(url_for("index"))

    conn = get_db_connection()
    abastecimentos = conn.execute("SELECT * FROM abastecimentos ORDER BY id DESC").fetchall()
    conn.close()

    lista = []
    for row in abastecimentos:
        consumo = row["km"] / row["litros"] if row["litros"] != 0 else 0
        lista.append({
            "id": row["id"],
            "data": row["data"],
            "litros": row["litros"],
            "valor": row["valor"],
            "km": row["km"],
            "consumo": consumo,
            "km_restante": row["km_restante"],
            "litros_restantes": row["litros_restantes"]
        })

    return render_template("index.html", abastecimentos=lista)

@app.route("/excluir/<int:id>")
def excluir(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM abastecimentos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("Registro excluído com sucesso!", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
