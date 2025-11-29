from app import db, login_manager
from datetime import date
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -----------------------------
# Usuário (ADM, almoxarife, Aluno/prof)
# -----------------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=True)
    genero = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # cpf = db.Column(db.String(14), unique=True, nullable=False)
    cpf = db.Column(db.String(14), unique=True)
    telefone = db.Column(db.String(20), nullable=True)
    
    tipo_usuario = db.Column(db.String(50), nullable=False, default="usuario") 
    senha = db.Column(db.String(200), nullable=False)
    
    imagem_perfil = db.Column(db.String(200), nullable=True) 
    
    def __repr__(self):
        return f"<User {self.nome} ({self.tipo_usuario})>"



class TipoProduto(db.Model):
    __tablename__ = 'tipo_produto'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<TipoProduto {self.nome}>'

class Fornecedor(db.Model):
    __tablename__ = 'fornecedor'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Fornecedor {self.nome}>'

class UnidadeMedida(db.Model):
    __tablename__ = 'unidade_medida'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<UnidadeMedida {self.nome}>'

class Produto(db.Model):
    __tablename__ = 'produto'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipo_produto.id'), nullable=True)
    tipo = db.relationship('TipoProduto', backref=db.backref('produtos', lazy=True))
    
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'), nullable=True)
    fornecedor = db.relationship('Fornecedor', backref=db.backref('produtos', lazy=True))
    
    quantidade = db.Column(db.Integer, nullable=False)
    data_entrada = db.Column(db.Date, nullable=False, default=date.today)
    
    unidade_medida_id = db.Column(db.Integer, db.ForeignKey('unidade_medida.id'), nullable=True)
    unidade_medida = db.relationship('UnidadeMedida', backref=db.backref('produtos', lazy=True))
    
    imagem = db.Column(db.String(200), nullable=True)  # caminho para a imagem

    def __repr__(self):
        return f'<Produto {self.nome}>'
    

class Solicitacao(db.Model):
    __tablename__ = 'solicitacao'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    
    # Chave estrangeira para disciplina
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplina.id'), nullable=True)
    disciplina = db.relationship('Disciplina', backref=db.backref('solicitacoes', lazy=True))
    
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"))
    quantidade = db.Column(db.Integer)
    data_limite = db.Column(db.Date)
    finalidade = db.Column(db.Text)

    def __repr__(self):
        return f'<Solicitacao {self.nome}>'
    

class Disciplina(db.Model):
    __tablename__ = 'disciplina'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False, unique=True)

    def __repr__(self):
        return f'<Disciplina {self.nome}>'



# -----------------------------
# 🟧 Modelo base (dados gerais)
# -----------------------------
class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    categoria = db.Column(db.String(30), nullable=False)  # transporte / limpeza / seguranca
    descricao = db.Column(db.Text, nullable=True)

    # Relação 1-1 com transporte
    transporte = db.relationship("ServiceTransporte", backref="service", uselist=False)

    def __repr__(self):
        return f"<Service {self.nome}>"

# -----------------------------
# 🚚 Serviço de Transporte (apenas os campos usados)
# -----------------------------
class ServiceTransporte(db.Model):
    __tablename__ = 'service_transporte'

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))

    # CAMPOS ESPECÍFICOS DO TRANSPORTE (somente os que vamos usar)
    tipo_veiculo = db.Column(db.String(60), nullable=True)
    quantidade_passageiros = db.Column(db.Integer, nullable=True)
    preco_diaria = db.Column(db.Float, nullable=True)


# -----------------------------
# 🚗 Tipos de Veículo
# -----------------------------
class TipoVeiculo(db.Model):
    __tablename__ = "tipo_veiculo"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
