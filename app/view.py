from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app import app
from app.forms import UserForm, LoginForm


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
            user = form.save()
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


@app.route('/cadastrar-produto')
def adicionar_produto():
    return render_template('cadastrar_produto.html')