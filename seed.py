from app import create_app, db
from app.models import Usuario, Veiculo, Cliente
from datetime import date

app = create_app()

def seed_database():
    with app.app_context():
        print("Limpando e recriando tabelas...")
        db.drop_all()
        db.create_all()
        
        admin = Usuario(
            nome='Administrador Murphy',
            cpf='000.000.000-01',
            email='admin@email.com',
            login='admin',
            senha='123',
            nivel='Administrador', 
            salario=5000.00
        )
        
        cliente = Cliente(
            nome='João da Silva',
            cpf='111.111.111-11',
            cnh='12345678910', 
            email='joao@email.com',
            telefone='(11) 98888-8888'
        )
        
        veiculo = Veiculo(
            modelo='Corolla',
            fabricante='Toyota',
            ano=2024,
            placa='ABC-1234',
            status='Disponível'
        )

        db.session.add_all([admin, cliente, veiculo])
        
        try:
            db.session.commit()
            print("✅ Sucesso! Tabelas recriadas e dados inseridos.")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro de integridade: {e}")

if __name__ == '__main__':
    seed_database()