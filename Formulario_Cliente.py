from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Criar a tabela no banco de dados (executar uma vez)
def create_table():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS responses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        empresa TEXT NOT NULL,
                        cidade TEXT NOT NULL,
                        telefone TEXT NOT NULL,
                        email TEXT NOT NULL,
                        viopex_choice TEXT NOT NULL,
                        viopex_choice2 TEXT NOT NULL,
                        concorrente_choice TEXT NOT NULL,
                        concorrente_choice2 TEXT NOT NULL,
                        concorrente_nome TEXT
                    )''')
    conn.commit()
    conn.close()

# Rota para o formulário
@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        nome = request.form['nome']
        empresa = request.form['empresa']
        cidade = request.form['cidade']
        telefone = request.form['telefone']
        email = request.form['email']
        viopex_choice = request.form['viopex_choice']
        viopex_choice2 = request.form['viopex_choice2']
        concorrente_choice = request.form['concorrente_choice']
        concorrente_choice2 = request.form['concorrente_choice2']
        concorrente_nome = request.form.get('concorrente_nome', '')

        # Salvar os dados no banco de dados
        conn = get_db_connection()
        conn.execute('''INSERT INTO responses (nome, empresa, cidade, telefone, email, 
                                              viopex_choice, viopex_choice2, concorrente_choice, 
                                              concorrente_choice2, concorrente_nome)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                     (nome, empresa, cidade, telefone, email, 
                      viopex_choice, viopex_choice2, concorrente_choice, 
                      concorrente_choice2, concorrente_nome))
        conn.commit()
        conn.close()

        return redirect(url_for('form'))

    return render_template('form.html')

# Rota para exibir os dados salvos no banco de dados
@app.route('/dados')
def listar_dados():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM responses').fetchall()
    conn.close()
    return render_template('dados.html', rows=rows)

if __name__ == '__main__':
    create_table()
    app.run(debug=True)