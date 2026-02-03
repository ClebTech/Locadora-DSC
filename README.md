# Locadora DSC

*Este é o módulo de gerenciamento de locação de veículos. O sistema utiliza uma arquitetura distribuída com Flask e MySQL para gerenciar usuários, clientes, veículos e contratos de aluguel.*

## Sobre o Projeto

Sistema de gerenciamento para locação de veículos desenvolvido para a disciplina de Arquitetura de Software. O projeto consiste na refatoração de um sistema legado  **[Locadora DSC](https://github.com/WallanMelo/Desenvolvimento-De-Sistemas-Corporativos-DSC-)** em Java para uma arquitetura moderna e distribuída utilizando Python, Flask e MySQL. 

## Arquitetura e Tecnologias

*O projeto utiliza o padrão Factory Pattern para inicialização da aplicação e Blueprints para modularização das rotas, garantindo escalabilidade e organização do código.*

* **Backend:** Flask (Python 3.12).
* **Banco de Dados:** MySQL com SQLAlchemy ORM.
* **Autenticação:** Flask-Login.
* **Frontend:** Jinja2 Templates & CSS3.


## Controle de Acesso (RBAC)

*O sistema implementa uma matriz de permissões baseada em níveis de acesso (Role-Based Access Control) para garantir a integridade dos dados:*

| Módulo | Administrador | Atendente | Mecânico |
| :--- | :--- | :--- | :--- |
| **Usuários** | Total | 🚫 | 🚫 |
| **Clientes** | Total | Criar/Listar | 🚫 |
| **Veículos** | Total | Listar | Editar/Criar |
| **Aluguéis** | Total | Operacional | 🚫 |


---

## Como Rodar o Projeto

*Você pode executar o projeto usando o gerenciador de pacotes padrão (`pip/venv`):*

### 1: Configuração do Ambiente

1. Clonar o repositório.
2. Acessar o diretório do projeto:
```bash
cd trabalho-arq-soft
```
3. Criar o ambiente virtual Python:
```bash
python3 -m venv .venv
```
4. Ativar o ambiente virtual:
*  `source .venv/bin/activate`
5. Instalar as dependências:
```bash
pip install -r requirements.txt
```

---

## Configuração da Infraestrutura

*Diferente da versão original, utilizamos scripts personalizados para garantir que o banco de dados MySQL reflita exatamente o *models.py*.*

1. Configuração da URI:
```bash
Certifique-se de que a senha do MySQL no arquivo app/__init__.py está correta para o seu ambiente local.
```
2. Criação e População do Banco:
*Execute o script de seed para criar as tabelas e inserir os dados iniciais de teste (Admin, Veículos e Clientes):*
```bash
python seed.py
```


---

## Executando a Aplicação

1. Inicie o servidor:
```bash
python run.py
```
2. Acesse no navegador: http://127.0.0.1:5000/

---

### Estrutura do Projeto

* `app/`: Pasta principal contendo o código fonte.
* `app/auth/, app/clientes/, app/alugueis/`: Módulos separados por Blueprints.
* `app/templates/`: Arquivos HTML organizados por módulos (Jinja2).
* `app/models.py`: Definição das tabelas MySQL (Usuario, Cliente, Veiculo, Aluguel).
* `seed.py`: Script de infraestrutura para reset e carga inicial de dados.
* `requirements.txt`: Lista de dependências do projeto.

## 👥 Equipe

| Integrante | Funções Principais | GitHub |
| :--- | :--- | :--- |
| **Geovana Rodrigues** | Arquitetura Modular, Modelagem de Dados, Automação de Ambiente e Persistência e Status | *[@murphiie](https://github.com/murphiie)* |
| **Clebson Santos** | Regras de Negócio, Gestão Operacional, Fluxo Financeiro e Relatórios | *[@ClebTech](https://github.com/ClebTech)* |


