from flask import Flask, escape, request, render_template

app = Flask(__name__)

@app.route('/ola')
def ola():
    return 'Olá'

@app.route('/')
def hello():
    name = request.args.get("name","world")
    return f'Hello, {escape(name)}!'

@app.route("/aula")
def teste():
    return '<h1>Programação para Internet II</h1>'

@app.route("/teste1")
def template():
    return render_template('teste1.html')

@app.route("/lista")
def lista():
    alunos = ['Leonel','Roberto','Cleusa']
    return render_template('teste1.html',alunos = alunos)

@app.route('/verifica/<nome>')
def verifica_nome(nome):
    alunos = ['Leonel','Roberto','Cleusa']
    return render_template('teste1.html',alunos = alunos, nome = nome)

if __name__ == '__main__':
    app.run(debug=True)
