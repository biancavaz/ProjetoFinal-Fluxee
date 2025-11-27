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
    

# -----------------------------
# 🟧 Modelo base (apenas dados gerais)
# -----------------------------
class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    categoria = db.Column(db.String(30), nullable=False)  # transporte / limpeza / seguranca
    descricao = db.Column(db.Text, nullable=True)

    # Relações 1-1 com os modelos específicos
    transporte = db.relationship("ServiceTransporte", backref="service", uselist=False)
    limpeza = db.relationship("ServiceLimpeza", backref="service", uselist=False)
    seguranca = db.relationship("ServiceSeguranca", backref="service", uselist=False)

    def __repr__(self):
        return f"<Service {self.nome}>"


# -----------------------------
# 🚚 Serviço de Transporte (dados específicos)
# -----------------------------
class ServiceTransporte(db.Model):
    __tablename__ = 'service_transporte'

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))

    # CAMPOS ESPECÍFICOS DO TRANSPORTE
    tipo_veiculo = db.Column(db.String(60))           
    capacidade = db.Column(db.Integer)                 
    quantidade_passageiros = db.Column(db.Integer)     
    quantidade_onibus = db.Column(db.Integer)          
    preco_diaria = db.Column(db.Float)                 
    data_saida = db.Column(db.Date)                    
    data_retorno = db.Column(db.Date)                  
    horario_saida = db.Column(db.Time)                 
    horario_chegada = db.Column(db.Time)      


# -----------------------------
# 🧼 Serviço de Limpeza (dados específicos)
# -----------------------------         
class ServiceLimpeza(db.Model):
    __tablename__ = 'service_limpeza'

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))

    # CAMPOS ESPECÍFICOS DA LIMPEZA
    tempo = db.Column(db.String(50))             # Ex: 2h, 1h30
    ambiente = db.Column(db.String(100))         # Local / área a ser limpa
    frequencia = db.Column(db.String(50))        # diária, semanal, mensal…
    periodo = db.Column(db.String(50))           # manhã, tarde, noite ou integral



# -----------------------------
# 🛡 Serviço de Segurança (dados específicos)
# -----------------------------
class ServiceSeguranca(db.Model):
    __tablename__ = 'service_seguranca'

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))

    # CAMPOS ESPECÍFICOS DA SEGURANÇA
    data_inicio = db.Column(db.Date)             # Data de início do serviço
    area_atuacao = db.Column(db.String(100))     # Área ou local de atuação
    turno = db.Column(db.String(50))             # Manhã, tarde, noite ou integral
    frequencia = db.Column(db.String(50)) 