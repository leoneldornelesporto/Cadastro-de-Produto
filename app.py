from flask import Flask, render_template, request, redirect, flash, url_for
import requests
from flask_sqlalchemy import SQLAlchemy
import locale
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Y0ur Secret Key Xmsnsnkd8939'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/mercado.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
UPLOAD_PATH = os.path.join(os.getcwd(), 'static/fotos/')

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    marca = db.Column(db.String(40), nullable=False)
    quant = db.Column(db.Integer)
    preco = db.Column(db.Float)

    def __repr__(self):
        return '<Produto %r>' % self.nome

@app.route('/')
def principal():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        # obtém os dados do form
        nome = request.form['nome']        
        marca = request.form['marca']        
        quant = request.form['quant']        
        preco = request.form['preco']        

        produto = Produto(nome=nome, 
                          marca=marca, 
                          quant=quant, 
                          preco=preco)        
        
        db.session.add(produto)
        db.session.commit()

        # obtém e salva a foto do produto
        foto = request.files['foto']
        destino = UPLOAD_PATH + str(produto.id) + '.jpg'
        foto.save(destino)

        flash(f'Ok! Produto {nome} cadastrado com sucesso!!')
        return redirect('/listagem')        
    return render_template('cadastro.html')

@app.route('/listagem')
def listagem():
    produtos = Produto.query.all()
    return render_template('listagem.html', lista_produtos=produtos)

@app.route('/balanco')
def balanco():    
    if db.session.query(Produto).count() == 0:
        num = 0
        media = 0
        total = 0
    else:
        # para formatação de moeda
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

        num = db.session.query(db.func.count(Produto.id)).first()[0]        

        db_media = db.session.query(db.func.avg(Produto.preco)).first()[0]
        media = locale.currency(db_media, grouping=True, symbol=None)

        db_total = db.session.query(db.func.sum(Produto.quant*Produto.preco)).first()[0]
        total = locale.currency(db_total, grouping=True, symbol=None)
        
    return render_template('balanco.html', num=num, 
                           media=media, 
                           total=total)


@app.route('/delete/<int:id>')
def delete(id):
    Produto.query.filter_by(id=id).delete()
    db.session.commit()
    
    # exclui a foto do produto
    os.remove('static/fotos/'+str(id)+'.jpg')
    
    # outra forma de usar o redirect (para o nome da def)
    return redirect(url_for('listagem'))        


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    produto = Produto.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('altera.html', 
                        id=produto.id, 
                        nome=produto.nome, 
                        marca=produto.marca, 
                        quant=produto.quant, 
                        preco=produto.preco)    
    else:
        produto.nome = request.form['nome']
        produto.marca = request.form['marca']
        produto.quant = request.form['quant']
        produto.preco = request.form['preco']

        db.session.commit()

        # se selecionou nova foto
        if request.files['foto']:
            # obtém e salva a foto do produto
            foto = request.files['foto']
            destino = UPLOAD_PATH + str(produto.id) + '.jpg'
            foto.save(destino)

        # outra forma de usar o redirect (para o nome da def)
        return redirect(url_for('listagem'))        

if __name__ == '__main__':
    app.run(debug=True)
