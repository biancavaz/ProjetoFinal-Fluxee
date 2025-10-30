from app import app, db, bcrypt
from app.models import User

def criar_admin():
    # Criar hash da senha
    senha_hash = bcrypt.generate_password_hash('admin123').decode('utf-8')

    # Criar usuário admin
    admin = User(
        nome='Admin',
        sobrenome='Principal',
        email='admin@teste.com',
        senha=senha_hash,
        tipo='admin'
    )

    # Salvar no banco
    db.session.add(admin)
    db.session.commit()
    print("Usuário admin criado com sucesso!")

if __name__ == "__main__":
    # ⚠️ Importante: ativar o contexto do app
    with app.app_context():
        criar_admin()
