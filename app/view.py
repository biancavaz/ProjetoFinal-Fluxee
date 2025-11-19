from datetime import date, datetime
import os
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app import app, db
from app.forms import UserForm, LoginForm
from app.models import Fornecedor, Produto, TipoProduto, UnidadeMedida, User
from werkzeug.utils import secure_filename

# Configurar pasta de upload
UPLOAD_FOLDER = 'static/uploads/produtos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# -------------------------
# LOGIN
# -------------------------
@app.route('/', methods=['GET', 'POST'])
def homepage():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = form.login()
            login_user(user, remember=True)
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('home'))
        except Exception as e:
            flash(str(e), "danger")
    return render_template('login.html', form=form, show_navbar=False)


# -------------------------
# CADASTRO DE USUÁRIO
# -------------------------
@app.route('/cadastro/', methods=['GET', 'POST'])
def cadastro():
    form = UserForm()

    if form.validate_on_submit():
        try:
            user = form.save()  # já salva e adiciona ao DB
            login_user(user, remember=True)
            flash("Cadastro realizado com sucesso!", "success")
            return redirect(url_for('homepage'))
        except Exception as e:
            flash(f"Erro ao cadastrar usuário: {str(e)}", "danger")

    elif request.method == "POST":
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Erro no campo '{getattr(form, field).label.text}': {error}", "danger")

    return render_template('cadastro.html', form=form, show_navbar=False)



# -------------------------
# LOGOUT
# -------------------------
@app.route('/logout/')
@login_required
def sair():
    logout_user()
    flash("Logout realizado com sucesso.", "info")
    return redirect(url_for('homepage'))


# -------------------------
# HOMEPAGE PRINCIPAL (após login)
# -------------------------
@app.route('/home/')
@login_required
def home():
    return render_template('home.html')


# -------------------------
# GESTÃO
# -------------------------
@app.route('/gestao/')
@login_required
def gestao():
    return render_template('gestao.html')

@app.route('/gestao_servico/')
@login_required
def gestao_servico():
    return render_template('gestao_servico.html')

# -------------------------
# MOVIMENTAÇÕES
# -------------------------
@app.route('/movimentacoes/')
@login_required
def movimentacoes():
    return render_template('movimentacoes.html')


# -------------------------
# SOLICITAÇÕES
# -------------------------
@app.route('/solicitacoes/')
@login_required
def solicitacoes():
    return render_template('solicitacoes.html')


# -------------------------
# CADASTRO DE PRODUTO
# -------------------------
@app.route('/cadastrar-produto', methods=['GET', 'POST'])
def adicionar_produto():
    tipos_produto = TipoProduto.query.all()  # Puxa do banco
    fornecedores = Fornecedor.query.all()
    unidades_medida = UnidadeMedida.query.all()

    if request.method == 'POST':
        nome = request.form.get('nome')
        tipo_id = request.form.get('tipo')
        fornecedor_id = request.form.get('fornecedor')
        unidade_id = request.form.get('unidade_medida')
        quantidade = request.form.get('quantidade')
        data_entrada_str = request.form.get('data_entrada')

        # Validar quantidade
        try:
            quantidade = int(quantidade)
        except (ValueError, TypeError):
            flash("Quantidade inválida.", "danger")
            return redirect(url_for('adicionar_produto'))

        # Tratar data
        if data_entrada_str:
            try:
                data_entrada = datetime.strptime(data_entrada_str, '%Y-%m-%d').date()
            except ValueError:
                data_entrada = date.today()
        else:
            data_entrada = date.today()

        # Upload de imagem
        arquivo = request.files.get('imagem')
        caminho_imagem = None
        if arquivo and arquivo.filename != '':
            filename = secure_filename(arquivo.filename)
            caminho_imagem = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            arquivo.save(caminho_imagem)

        produto = Produto(
            nome=nome,
            tipo_id=tipo_id if tipo_id else None,
            fornecedor_id=fornecedor_id if fornecedor_id else None,
            unidade_medida_id=unidade_id if unidade_id else None,
            quantidade=quantidade,
            data_entrada=data_entrada,
            imagem=caminho_imagem
        )

        db.session.add(produto)
        db.session.commit()
        flash("Produto cadastrado com sucesso!", "success")
        return redirect(url_for('adicionar_produto'))

    # Converter para listas de tuplas (id, nome) para usar nos dropdowns
    tipos_produto_dropdown = [(t.id, t.nome) for t in tipos_produto]
    fornecedores_dropdown = [(f.id, f.nome) for f in fornecedores]
    unidades_medida_dropdown = [(u.id, u.nome) for u in unidades_medida]

    return render_template(
        'cadastrar_produto.html',
        tipos_produto=tipos_produto_dropdown,
        fornecedores=fornecedores_dropdown,
        unidades_medida=unidades_medida_dropdown
    )



# -------------------------
# CADASTRO DE SERVIÇO
# -------------------------
@app.route('/cadastrar-servico', methods=['GET', 'POST'])
def adicionar_servico():
   return render_template('cadastrar_servico.html')



# -------------------------
# GESTÃO - USUÁRIOS
# -------------------------
@app.route('/usuarios/')
@login_required
def usuarios():
    return render_template('usuarios.html')


# -------------------------
# CADASTRO DE SERVIÇO
# -------------------------

@app.route('/cadastrar-usuarios', methods=['GET', 'POST'])
def adicionar_usuario():
    
    generos = ["Masculino", "Feminino", "Outro", "Prefiro não informar"]
    tipos_usuario = ["Administrador", "Almoxarife", "Professor/Representante de sala", "terceiro"]

    if request.method == 'POST':
        nome = request.form.get('nome')
        data_nascimento_str = request.form.get('data_nascimento')
        genero = request.form.get('genero')
        email = request.form.get('email')
        cpf = request.form.get('cpf')
        telefone = request.form.get('telefone')
        tipo_usuario = request.form.get('tipo_usuario')

        # Converter data
        try:
            data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()
        except:
            data_nascimento = None

        # Verifica se enviou arquivo
        imagem_file = request.files.get('imagem_perfil')
        caminho_imagem = None
        if imagem_file and imagem_file.filename != '':
            nome_seguro = secure_filename(imagem_file.filename)
            caminho_imagem = os.path.join(app.config['UPLOAD_FOLDER'], nome_seguro)
            # cria pasta se não existir
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            imagem_file.save(caminho_imagem)

        # Criar novo usuário
        novo_usuario = User(
            nome=nome,
            data_nascimento=data_nascimento,
            genero=genero,
            email=email,
            cpf=cpf,
            telefone=telefone,
            tipo_usuario=tipo_usuario,
            senha="senha_temporaria",
            imagem_perfil=caminho_imagem  # salva caminho da imagem no DB
        )

        db.session.add(novo_usuario)
        db.session.commit()

        flash("Usuário cadastrado com sucesso!", "success")
        return redirect(url_for('adicionar_usuario'))

    return render_template(
        'cadastrar_usuarios.html',
        generos=generos,
        tipos_usuario=tipos_usuario
    )

