# controllers/item_controller.py
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from models.Base import SessionLocal
from models.Item import Item
from models.List import List

item_bp = Blueprint('item_bp', __name__, url_prefix='/items')

@item_bp.route('/<int:list_id>')
@login_required
def list_items(list_id):
    print(f'Listando itens da lista {list_id}')
    with SessionLocal() as session:
        items = session.query(Item).filter_by(list_id=list_id).all()
        lista = session.query(List).filter_by(id=list_id).first()
    return render_template('items.html', items=items, list_id=list_id, lista=lista)


@item_bp.route('/create', methods=['POST'])
@login_required
def create_item():
    """Cria um novo item, associando a uma lista."""
    item_name = request.form.get('item_name')
    list_id = request.form.get('list_id')
    session = SessionLocal()
    lista = session.query(List).filter_by(id=list_id).first()
    list_id = lista.id if lista else None

    print(f'Item {item_name} criado na lista {list_id}')
    if lista and item_name:
        new_item = Item(name=item_name, list_id=lista.id)
        session.add(new_item)
        session.commit()
    if not item_name:
        flash('Nome do item é obrigatório', 'error')
        return redirect(url_for('list_bp.open_list', list_id=list_id))
    if not lista:
        flash('Lista não encontrada', 'error')
        return redirect(url_for('list_bp.list_lists'))
    
    session.close()
    return redirect(url_for('item_bp.list_items', list_id=list_id))

@item_bp.route('/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    """Remove um item."""
    session = SessionLocal()
    item = session.query(Item).filter_by(id=item_id).first()
    print(f'Item {item}')
    if item:
        session.delete(item)
        session.commit()
    else:
        flash(f'Item não encontrado ({item_id})')
        return redirect(url_for('item_bp.list_items', list_id=item.list_id))
    session.close()
    print(f'Item {item} removido')
    return redirect(url_for('item_bp.list_items', list_id=item.list_id))

@item_bp.route('/toggle/<int:item_id>', methods=['POST'])
@login_required
def toggle_item(item_id):
    session = SessionLocal()
    item = session.query(Item).filter_by(id=item_id).first()
    if not item:
        flash(f'Item não encontrado ({item_id})')
        session.close()
        return redirect(url_for('list_bp.list_lists'))

    # Verifica se o checkbox veio marcado
    is_checked = request.form.get('is_checked')  # "on" se estiver marcado, None se não
    item.check = 1 if is_checked == 'on' else 0
    
    session.commit()
    list_id = item.list_id
    session.close()

    return redirect(url_for('item_bp.list_items', list_id=list_id))
