from app import app, db
from app.models import TipoProduto, Fornecedor, UnidadeMedida

# Criar o contexto da aplicação
with app.app_context():

    # Verifica se já existe, para não duplicar
    if not TipoProduto.query.first():
        db.session.add_all([
            TipoProduto(nome="material escolar"),
        ])

    if not Fornecedor.query.first():
        db.session.add_all([ 
            Fornecedor(nome="Fornecedor A"),
            Fornecedor(nome="Fornecedor B"),
            Fornecedor(nome="Fornecedor C")
        ])

    if not UnidadeMedida.query.first():
        db.session.add_all([
            UnidadeMedida(nome="KG"),
            UnidadeMedida(nome="UN"),
            UnidadeMedida(nome="G"),
            UnidadeMedida(nome="CM"),
            UnidadeMedida(nome="L"),
            UnidadeMedida(nome="ML")
        ])

    db.session.commit()
    print("Valores padrões inseridos com sucesso!")
