from functools import wraps
from flask import session, redirect, url_for, flash
from flask_login import current_user


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("homepage"))

        if session.get("tipo_usuario") != "admin":
            flash("Acesso negado! Apenas administradores podem acessar.", "danger")
            return redirect(url_for("home"))

        return f(*args, **kwargs)
    return wrapper


def professor_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("homepage"))

        if session.get("tipo_usuario") not in ("professor", "admin"):
            flash("Acesso restrito a professores.", "danger")
            return redirect(url_for("home"))

        return f(*args, **kwargs)
    return wrapper
