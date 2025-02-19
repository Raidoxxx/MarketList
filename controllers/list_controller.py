# controllers/list_controller.py

from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from models.Base import SessionLocal
from models.List import List
from models.Item import Item

list_bp = Blueprint('list_bp', __name__, url_prefix='/lists')

@list_bp.route('/')
@login_required
def list_lists():
    """Lista todas as listas de um usuário."""
    session = SessionLocal()
    print(f'Current user: {current_user.id}')
    lists = session.query(List).filter_by(user_id=current_user.id).all()
    session.close()
    return render_template('lists.html', lists=lists)

@list_bp.route('/create', methods=['POST'])
@login_required
def create_list():
    """Cria uma nova lista."""
    list_name = request.form.get('list_name')
    if not list_name:
        flash('Nome da lista é obrigatório', 'error')
        return redirect(url_for('list_bp.list_lists'))
    session = SessionLocal()
    new_list = List(name=list_name, user_id=current_user.id)
    session.add(new_list)
    session.commit()
    session.close()
    return redirect(url_for('list_bp.list_lists', user_id=current_user.id))

@list_bp.route('/delete/<int:list_id>', methods=['POST'])
@login_required
def delete_list(list_id):
    """Remove uma lista."""
    session = SessionLocal()
    l = session.query(List).filter_by(id=list_id).first()
    if l:
        session.delete(l)
        session.commit()
    session.close()
    return redirect(url_for('list_bp.list_lists'))

@list_bp.route('/<int:list_id>')
@login_required
def open_list(list_id):
    """Mostra os itens de uma lista."""
    session = SessionLocal()
    lista = session.query(List).filter_by(id=list_id).first()
    items = session.query(Item).filter_by(list_id=list_id).all()
    return render_template('items.html', items=items, list_id=list_id, lista=lista)