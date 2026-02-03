from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Aluguel, Veiculo, Cliente, Manutencao, Pagamento
from app import db
from datetime import datetime, date

alugueis_bp = Blueprint('alugueis', __name__)

@alugueis_bp.route('/alugueis/novo', methods=['GET', 'POST'])
def novo():
    if request.method == 'POST':
        veiculo_id = request.form.get('veiculo_id')
        cliente_id = request.form.get('cliente_id')
        data_devolucao_str = request.form.get('data_devolucao')

        veiculo = Veiculo.query.get(veiculo_id)
        
        if veiculo:
            novo_aluguel = Aluguel(
                cliente_id=cliente_id,
                veiculo_id=veiculo_id,
                data_inicio=date.today(),
                prazo_devolucao=datetime.strptime(data_devolucao_str, '%Y-%m-%d').date(),
                valor=150.00
            )
            
            veiculo.status = 'Alugado'
            
            db.session.add(novo_aluguel)
            db.session.commit()
            
            flash(f'Aluguel do {veiculo.modelo} realizado com sucesso!')
            return redirect(url_for('alugueis.historico'))
    
    carros = Veiculo.query.filter_by(status='Disponível').all()
    pessoas = Cliente.query.all()
    return render_template('alugueis/novo_aluguel.html', veiculos=carros, clientes=pessoas)

@alugueis_bp.route('/alugueis/historico')
def historico():
    lista_alugueis = Aluguel.query.all()
    return render_template('alugueis/historico.html', alugueis=lista_alugueis)

@alugueis_bp.route('/alugueis/devolver/<int:id>')
def devolver(id):
    aluguel = Aluguel.query.get_or_404(id)
    veiculo = Veiculo.query.get(aluguel.veiculo_id)

    if aluguel and veiculo:
        aluguel.devolvido = True
        aluguel.data_fim = date.today()
        veiculo.status = 'Disponível'
        
        db.session.commit()
        flash(f'Veículo {veiculo.modelo} devolvido com sucesso!')
    
    return redirect(url_for('alugueis.historico'))