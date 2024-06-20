from flask import Flask, render_template, request, redirect, url_for
import sqlite3

class Livro:
    def __init__(self, titulo: str, autor: str, genero: str):
        self.titulo = titulo
        self.autor = autor
        self.genero = gener

class Biblioteca:
    def __init__(self):
        self.criar_tabela()

    def criar_tabela(self):
        connection = sqlite3.connect('biblioteca.db')
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY,
                titulo TEXT,
                autor TEXT,
                genero TEXT
            )
        ''')
        connection.commit()
        connection.close()

    def exibir_livros(self):
        connection = sqlite3.connect('biblioteca.db')
        cursor = connection.cursor()
        cursor.execute('''
            SELECT * FROM livros
        ''')
        livros = cursor.fetchall()
        connection.close()
        return livros
       
    def adicionar_livro(self, livro: Livro):
        connection = sqlite3.connect('biblioteca.db')
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO livros (titulo, autor, genero) VALUES (?, ?, ?)
        ''', (livro.titulo, livro.autor, livro.genero))
        connection.commit()
        connection.close()

    def remover_livro(self, id):
        connection = sqlite3.connect('biblioteca.db')
        cursor = connection.cursor()
        cursor.execute('''
            DELETE FROM livros WHERE id = ?
        ''', (id,))
        connection.commit()
        connection.close()

    def editar_livro(self, id, titulo, autor, genero):
        connection = sqlite3.connect('biblioteca.db')
        cursor = connection.cursor()

        query = "UPDATE livros SET "
        updates = []
        params = []

        if titulo:
            updates.append('titulo = ?')
            params.append(titulo)
        if autor:
            updates.append('autor = ?')
            params.append(autor)
        if genero:
            updates.append('genero = ?')
            params.append(genero)

        query += ', '.join(updates)

        query += ' WHERE id = ?'
        params.append(id)

        cursor.execute(query, params)
        connection.commit()
        connection.close()

    def pesquisar_livros(self, titulo, autor, genero):
        connection = sqlite3.connect('biblioteca.db')
        cursor = connection.cursor()

        query = "SELECT * FROM livros WHERE "
        updates = []
        params = []

        if titulo:
            updates.append('titulo LIKE ?')
            params.append('%' + titulo + '%')
        if autor:
            updates.append('autor LIKE ?')
            params.append('%' + autor + '%')
        if genero:
            updates.append('genero LIKE ?')
            params.append('%' + genero + '%')

        if (len(params) == 0):
            connection.close()
            return self.exibir_livros()

        query += 'AND '.join(updates)

        cursor.execute(query, params)
        livros = cursor.fetchall()
        connection.close()
        return livros

biblioteca = Biblioteca()

app = Flask(__name__)

@app.route('/')
def livros():
    livros = biblioteca.exibir_livros()
    return render_template('livros.html', livros=livros)

@app.route('/adicionar-livro', methods=['POST'])
def adicionar_livro():
    titulo = request.form['titulo']
    autor = request.form['autor']
    genero = request.form['genero']
    biblioteca.adicionar_livro(Livro(titulo, autor, genero))
    return redirect(url_for('livros'))

if __name__ == "__main__":
    app.run(debug=True)
