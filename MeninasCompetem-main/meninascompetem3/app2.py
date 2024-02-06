from flask import Flask, jsonify, render_template, request, redirect, url_for
import sqlite3
import pandas as pd

app = Flask(__name__)

DATABASE = 'comp2.db'

def criar_tabela():
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS usuarios(id integer PRIMARY KEY, nome TEXT NOT NULL, site TEXT NOT NULL, descricao TEXT NOT NULL, data_final DATE, valor TEXT NOT NULL, nivel TEXT NOT NULL, categoria TEXT NOT NULL)')
        con.commit()

criar_tabela()



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pagina_inicial.html')
def pagina_inicial():
    return render_template('pagina_inicial.html')

@app.route('/pagina_um.html')
def pagina_um():
    return render_template('pagina_um.html')


def filtragem(categorias):
    with sqlite3.connect(DATABASE) as con:
        placeholders_categoria = ",".join(["?"] * len(categorias))
        query = f"SELECT * FROM usuarios WHERE categoria IN ({placeholders_categoria})"
        params = tuple(categorias)
        df = pd.read_sql(query, con, params=params)
    return df

def filtragem(categorias):
    with sqlite3.connect(DATABASE) as con:
        placeholders_categoria = ",".join(["?"] * len(categorias))
        query = f"SELECT * FROM usuarios WHERE categoria IN ({placeholders_categoria})"
        params = tuple(categorias)
        df = pd.read_sql(query, con, params=params)
    return df

def search(termo):
    with sqlite3.connect(DATABASE) as con:
        query = "SELECT * FROM usuarios WHERE nome LIKE ? OR descricao LIKE ?"
        params = ('%' + termo + '%', '%' + termo + '%')
        df = pd.read_sql(query, con, params=params)
    return df


@app.route('/pagina_dois', methods=['GET', 'POST'])
def pagina_dois():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            search_term = data.get('search_term', '')
            if search_term:
                # Perform search based on the search term
                dataframe = search(search_term)
                return jsonify(dataframe.to_dict(orient='records'))
            else:
                # If no search term provided, return all data
                categorias = data.get('categoria', [])
                dataframe = filtragem(categorias)
                return jsonify(dataframe.to_dict(orient='records'))
        else:
            return jsonify({'error': 'Invalid JSON format'})
    else:
        # Handle GET request (rendering the template)
        return render_template('pagina_dois.html')


@app.route('/seu-script-de-processamento', methods=['POST'])
def processar_formulario():
    nome = request.form.get('nome')
    site = request.form.get('site')
    descricao = request.form.get('descricao')
    data_final = request.form.get('data_final')
    valor = request.form.get('valor')
    nivel = request.form.getlist('nivel')
    nivel_str = ', '.join(nivel)
    categoria = request.form.get('categoria')

    

    if nome and site and descricao and categoria and data_final and valor and nivel and categoria is not None:
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            id
            cur.execute('INSERT INTO usuarios (nome, site, descricao, data_final, valor, nivel, categoria) VALUES (?,?,?,?,?,?,?)', (nome, site, descricao, data_final, valor, nivel_str, categoria))
            con.commit()
            return redirect(url_for('index'))
    return redirect(url_for('index'))

def new_func(nivel):
    return nivel


if __name__ == '__main__':
    app.run(debug=True)