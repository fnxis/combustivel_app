from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # necessário para flash messages

DB = 'abastecimentos.db'

def get_db_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabela():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS abastecimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            litros REAL,
            valor REAL,
            km REAL
        )
    """)
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

            conn = get_db_connection()
            conn.execute("INSERT INTO abastecimentos (data, litros, valor, km) VALUES (?, ?, ?, ?)",
                         (data, litros, valor, km))
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

    # Calcular consumo e dados de combustível restante para exibir
    lista = []
    for row in abastecimentos:
        consumo = row["km"] / row["litros"] if row["litros"] != 0 else 0
        km_total = row["litros"] * 10
        km_restante = max(0, km_total - row["km"])
        litros_restantes = max(0, km_restante / 10)
        lista.append({
            "id": row["id"],
            "data": row["data"],
            "litros": row["litros"],
            "valor": row["valor"],
            "km": row["km"],
            "consumo": consumo,
            "km_total": km_total,
            "km_restante": km_restante,
            "litros_restantes": litros_restantes
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
    app.run(debug=True)
