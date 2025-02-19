# controllers/user_controller.py
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.Base import SessionLocal
from models.User import User

user_bp = Blueprint('user_bp', __name__, url_prefix='/users')

@user_bp.route('/')
@login_required
def list_users():
    session = SessionLocal()
    users = session.query(User).all()
    session.close()
    return render_template('users.html', users=users)

@user_bp.route('/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        session = SessionLocal()

        if not name or not email or not password:
            flash('Todos os campos são obrigatórios', 'error')
            return redirect(url_for('user_bp.create_user'))
        
        if session.query(User).filter_by(email=email).first():
            flash('Email já cadastrado', 'error')
            return redirect(url_for('user_bp.create_user'))

        new_user = User(name=name, email=email)
        new_user.set_password(password)
        session.add(new_user)
        session.commit()
        session.close()
        flash('Usuário criado com sucesso', 'success')
        return redirect(url_for('list_bp.list_lists'))
    else:
        return render_template('create_user.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('list_bp.list_lists'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        session = SessionLocal()
        user = session.query(User).filter_by(email=email).first()
        session.close()
        if not email or not password:
            flash('Preencha todos os campos', 'error')
            return redirect(url_for('user_bp.login'))

        if user and user.check_password(password):
            login_user(user)
            flash('Login realizado com sucesso', 'success')
            return redirect(url_for('list_bp.list_lists'))
        else:
            flash('Email ou senha incorretos', 'error')
            return redirect(url_for('user_bp.login'))
    else:
        return render_template('login.html')

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso', 'success')
    return redirect(url_for('user_bp.login'))

@user_bp.route('/forgot_password')
def forgot_password():
    return "Esqueceu a senha?"
