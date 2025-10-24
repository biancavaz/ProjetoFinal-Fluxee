from app import db, login_manager
from flask_login import UserMixin


# -----------------------------
# Função usada pelo Flask-Login
# -----------------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -----------------------------
# Modelo de Usuário
# -----------------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # ADM, BIBLIOTECARIO, ALUNO

    def __repr__(self):
        return f"<User {self.nome} ({self.tipo})>"
