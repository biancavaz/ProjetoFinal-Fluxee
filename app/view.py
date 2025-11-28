from datetime import date, datetime
import os
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app import app, db
from app.forms import UserForm, LoginForm
from app.models import Fornecedor, Produto, Service, ServiceLimpeza, ServiceSeguranca, ServiceTransporte, TipoProduto, TipoVeiculo, UnidadeMedida, User, Solicitacao

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash


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
    page = request.args.get('page', 1, type=int)
    per_page = 15
    produtos_pag = Produto.query.paginate(page=page, per_page=per_page)

    mostrar_paginacao = produtos_pag.total >= per_page

    return render_template(
        'gestao.html',
        produtos=produtos_pag.items,
        pagination=produtos_pag,
        mostrar_paginacao=mostrar_paginacao,
        pagina_atual=page  # <--- passa a página atual
    )



@app.route('/gestao_servico/')
@login_required
def gestao_servico():
    return render_template('gestao_servico.html')


@app.route('/produto/editar/<int:id>')
@login_required
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    return render_template('editar_produto.html', produto=produto)


@app.route('/produto/deletar/<int:id>')
@login_required
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('gestao'))


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

from sqlalchemy import func
@app.route('/dashboard/')
@login_required
def dashboard():
    result = db.session.query(
        TipoProduto.nome,             # Pega o nome da categoria
        func.count(Produto.id)
    ).join(Produto.tipo).group_by(TipoProduto.nome).all()

    # Converte para lista de dicionários
    tipo_counts = [{"tipo": tipo, "count": count} for tipo, count in result]

    tot_produto = len(Produto.query.all())
    tot_fornecedor = len(Fornecedor.query.all())
    tot_user = len(User.query.all())
    tot_servico = 0
    tot_solicitacao = 0

    return render_template('dashboard.html', tipo_counts=tipo_counts, tots={"produto":tot_produto, "fornecedor":tot_fornecedor, "user":tot_user, "servico":tot_servico, "solicitacao":tot_solicitacao})

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
        nome_arquivo = None
        UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads', 'produtos')
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # cria a pasta se não existir

        if arquivo and arquivo.filename != '':
            nome_arquivo = secure_filename(arquivo.filename)
            caminho_imagem = os.path.join(UPLOAD_FOLDER, nome_arquivo)
            arquivo.save(caminho_imagem)


        produto = Produto(
            nome=nome,
            tipo_id=tipo_id if tipo_id else None,
            fornecedor_id=fornecedor_id if fornecedor_id else None,
            unidade_medida_id=unidade_id if unidade_id else None,
            quantidade=quantidade,
            data_entrada=data_entrada,
            imagem=nome_arquivo  # <-- salvar só o nome do arquivo
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
# CADASTRO DE SOLICITACAO
# -------------------------
@app.route('/cadastrar-solicitacao', methods=['GET', 'POST'])
def adicionar_solicitacao():
    
    if request.method == 'POST':
        print(request.form)
        nome = request.form.get('nome')
        produto_id = request.form.get('produto_id')
        quantidade = request.form.get('quantidade')
        data_entrada_str = request.form.get('data_entrada_str')
        quantidade = request.form.get('quantidade')
        finalidade = request.form.get('finalidade')

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


        produto = Solicitacao(
            nome=nome,
            produto_id=produto_id if produto_id else None,
            data_limite=data_entrada if data_entrada else None,
            quantidade=quantidade if quantidade else None,
            finalidade=finalidade if finalidade else None,
        )

        db.session.add(produto)
        db.session.commit()
        flash("Produto cadastrado com sucesso!", "success")
        return redirect(url_for('adicionar_solicitacao'))


    # Converter para listas de tuplas (id, nome) para usar nos dropdowns
    produtos = [(p.id, p.nome) for p in Produto.query.all()]

    return render_template(
        'cadastrar_solicitacao.html',
        produtos=produtos,
    )



# -------------------------
# CADASTRO DE SERVIÇO
# -------------------------
@app.route('/cadastrar-servico', methods=['GET', 'POST'])
def cadastrar_servico():

    if request.method == 'POST':

        # -------------------------
        # CAMPOS GERAIS DO SERVICE
        # -------------------------
        nome = request.form.get('nome')
        categoria = request.form.get('categoria')   # transporte / limpeza / seguranca
        descricao = request.form.get('descricao')

        # Criar a entrada na tabela base
        service = Service(
            nome=nome,
            categoria=categoria,
            descricao=descricao
        )
        db.session.add(service)
        db.session.flush()   # pega o ID antes do commit


        # ===========================================
        # 🚚 CATEGORIA: TRANSPORTE
        # ===========================================
        if categoria == "transporte":

            transporte = ServiceTransporte(
                service_id=service.id,

                tipo_veiculo = request.form.get('tipo_veiculo'),
                capacidade = request.form.get('capacidade') or None,
                quantidade_passageiros = request.form.get('quantidade_passageiros') or None,
                quantidade_onibus = request.form.get('quantidade_onibus') or None,
                preco_diaria = request.form.get('preco_diaria') or None,

                data_saida = datetime.strptime(
                    request.form.get('data_saida'), "%Y-%m-%d"
                ).date() if request.form.get('data_saida') else None,

                data_retorno = datetime.strptime(
                    request.form.get('data_retorno'), "%Y-%m-%d"
                ).date() if request.form.get('data_retorno') else None,

                horario_saida = datetime.strptime(
                    request.form.get('horario_saida'), "%H:%M"
                ).time() if request.form.get('horario_saida') else None,

                horario_chegada = datetime.strptime(
                    request.form.get('horario_chegada'), "%H:%M"
                ).time() if request.form.get('horario_chegada') else None,
            )

            db.session.add(transporte)


        # ===========================================
        # 🧼 CATEGORIA: LIMPEZA
        # ===========================================
        elif categoria == "limpeza":

            limpeza = ServiceLimpeza(
                service_id=service.id,

                tempo = request.form.get('tempo'),
                ambiente = request.form.get('ambiente'),
                frequencia = request.form.get('frequencia'),
                periodo = request.form.get('periodo'),
            )

            db.session.add(limpeza)


        # ===========================================
        # 🛡 CATEGORIA: SEGURANÇA
        # ===========================================
        elif categoria == "seguranca":

            seguranca = ServiceSeguranca(
                service_id=service.id,

                data_inicio = datetime.strptime(
                    request.form.get('data_inicio'), "%Y-%m-%d"
                ).date() if request.form.get('data_inicio') else None,

                area_atuacao = request.form.get('area_atuacao'),
                turno = request.form.get('turno'),
                frequencia = request.form.get('frequencia'),
            )

            db.session.add(seguranca)


        # SALVAR TUDO
        db.session.commit()
        flash("Serviço cadastrado com sucesso!", "success")
        return redirect(url_for('cadastrar_servico'))


    # GET — carregar dropdowns
    tipos_veiculo = TipoVeiculo.query.all()

    return render_template(
        'cadastrar_servico.html',
        tipos_veiculo=tipos_veiculo
    )


# -------------------------
# GESTÃO - USUÁRIOS
# -------------------------
@app.route('/usuarios/')
@login_required
def usuarios():
    pagina_atual = request.args.get('page', 1, type=int)
    por_pagina = 10
    pagination = User.query.order_by(User.id).paginate(page=pagina_atual, per_page=por_pagina)
    usuarios = pagination.items
    mostrar_paginacao = pagination.pages > 1

    return render_template(
        'usuarios.html',
        usuarios=usuarios,
        pagination=pagination,
        pagina_atual=pagina_atual,
        mostrar_paginacao=mostrar_paginacao
    )


# Editar usuário
@app.route('/usuarios/editar/<int:id>')
@login_required
def editar_usuario(id):
    usuario = User.query.get_or_404(id)
    return render_template('editar_usuario.html', usuario=usuario)


# Deletar usuário
@app.route('/usuarios/deletar/<int:id>')
@login_required
def deletar_usuario(id):
    usuario = User.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('usuarios'))


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

        imagem_file = request.files.get('imagem_perfil')
        nome_imagem = None
        UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads', 'usuarios')
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        if imagem_file and imagem_file.filename != '':
            nome_seguro = secure_filename(imagem_file.filename)
            caminho_completo = os.path.join(UPLOAD_FOLDER, nome_seguro)
            imagem_file.save(caminho_completo)
            nome_imagem = nome_seguro  # só salva o nome no banco

        novo_usuario = User(
            nome=nome,
            data_nascimento=data_nascimento,
            genero=genero,
            email=email,
            cpf=cpf,
            telefone=telefone,
            tipo_usuario=tipo_usuario,
            senha=generate_password_hash("senha_temporaria"),
            imagem_perfil=nome_imagem  # agora vai funcionar no template
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

