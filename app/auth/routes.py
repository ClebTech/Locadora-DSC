from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models import Usuario, Cliente, Veiculo, Aluguel, Manutencao, Pagamento
from app import db
from . import auth_bp
from sqlalchemy import func

@auth_bp.route('/')
@login_required
def index():
    stats = {
        'total_clientes': Cliente.query.count(),
        'veiculos_disponiveis': Veiculo.query.filter_by(status='Disponível').count(),
        'veiculos_alugados': Veiculo.query.filter_by(status='Alugado').count(),
        'faturamento_total': db.session.query(func.sum(Aluguel.valor + Aluguel.multa)).scalar() or 0
    }
    return render_template('index.html', stats=stats)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form['login']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(login=login_input).first()

        if usuario and usuario.senha == senha:
            login_user(usuario)
            return redirect(url_for('auth.index')) 
        else:
            flash('Login ou senha inválidos')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))