from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, send_file
from flask_login import login_required, current_user
from app.models import Aluguel, Veiculo, Cliente, Manutencao, Pagamento
from app import db
from datetime import datetime, date
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

alugueis_bp = Blueprint('alugueis', __name__)

@alugueis_bp.route('/alugueis/novo', methods=['GET', 'POST'])
@login_required
def novo():
    if current_user.nivel not in ['Administrador', 'Atendente']:
        abort(403)

    if request.method == 'POST':
        veiculo_id = request.form.get('veiculo_id')
        cliente_id = request.form.get('cliente_id')
        data_devolucao_str = request.form.get('data_devolucao')

        veiculo = Veiculo.query.get(veiculo_id)
        
        if veiculo:
            try:
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
            except Exception as e:
                db.session.rollback()
                flash(f"Erro ao processar aluguel: {e}")
    
    carros = Veiculo.query.filter_by(status='Disponível').all()
    pessoas = Cliente.query.all()
    return render_template('alugueis/novo_aluguel.html', veiculos=carros, clientes=pessoas)

@alugueis_bp.route('/alugueis/historico')
@login_required
def historico():
    if current_user.nivel not in ['Administrador', 'Atendente']:
        flash("Acesso restrito ao setor de atendimento.")
        return redirect(url_for('auth.index'))
        
    lista_alugueis = Aluguel.query.all()
    return render_template('alugueis/historico.html', alugueis=lista_alugueis)

@alugueis_bp.route('/alugueis/devolver/<int:id>')
@login_required
def devolver(id):
    if current_user.nivel not in ['Administrador', 'Atendente']:
        abort(403)

    aluguel = Aluguel.query.get_or_404(id)
    veiculo = Veiculo.query.get(aluguel.veiculo_id)

    if aluguel and veiculo:
        aluguel.devolvido = True
        aluguel.data_fim = date.today()
        veiculo.status = 'Disponível'
        
        db.session.commit()
        flash(f'Veículo {veiculo.modelo} devolvido com sucesso!')
    
    return redirect(url_for('alugueis.historico'))

@alugueis_bp.route('/alugueis/relatorio/pdf')
@login_required
def gerar_pdf():
    if current_user.nivel not in ['Administrador', 'Atendente']:
        abort(403)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "Locadora DSC - Relatório de Aluguéis")
    
    p.setFont("Helvetica", 12)
    p.drawString(100, 730, f"Gerado por: {current_user.nome} em {date.today()}")
    p.line(100, 720, 500, 720)

    alugueis = Aluguel.query.all()
    y = 700
    for a in alugueis:
        status = "Devolvido" if a.devolvido else "Ativo"
        p.drawString(100, y, f"ID: {a.id} | Veículo ID: {a.veiculo_id} | Valor: R$ {a.valor} | Status: {status}")
        y -= 20
        if y < 50:
            p.showPage()
            y = 750

    p.showPage()
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='relatorio_alugueis.pdf', mimetype='application/pdf')