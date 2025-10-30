from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app import app
from app.forms import UserForm, LoginForm


# -------------------------
# HOME / LOGIN
# -------------------------
@app.route('/', methods=['GET', 'POST'])
def homepage():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = form.login()
            login_user(user, remember=True)
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('home'))  # redireciona para a mesma página ou outra
        except Exception as e:
            flash(str(e), "danger")  # erro de login
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
# HOMEPAGE (nova rota)
# -------------------------
@app.route('/home/')
@login_required
def home():
    return render_template('home.html')

