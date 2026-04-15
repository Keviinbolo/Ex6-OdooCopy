from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from models import db, Contact

# Crear blueprint para contactos
contacts_bp = Blueprint('contacts', __name__)

@contacts_bp.route('/apps')
@login_required
def apps():
    """Pantalla de aplicaciones"""
    return render_template('apps.html')

@contacts_bp.route('/contacts')
@login_required
def contacts_list():
    """Listar todos los contactos del usuario"""
    user_contacts = Contact.query.filter_by(user_id=current_user.id).order_by(Contact.name).all()
    return render_template('contacts.html', contacts=user_contacts)

@contacts_bp.route('/contacts/new', methods=['GET', 'POST'])
@login_required
def contact_new():
    """Crear nuevo contacto"""
    if request.method == 'POST':
        contact = Contact(
            name=request.form.get('name'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            company=request.form.get('company'),
            position=request.form.get('position'),
            notes=request.form.get('notes'),
            user_id=current_user.id
        )
        db.session.add(contact)
        db.session.commit()
        flash(f'Contacto "{contact.name}" creado exitosamente', 'success')
        return redirect(url_for('contacts.contacts_list'))
    
    return render_template('contact_form.html', contact=None)

@contacts_bp.route('/contacts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def contact_edit(id):
    """Editar contacto existente"""
    contact = Contact.query.get_or_404(id)
    
    # Verificar que el contacto pertenece al usuario actual
    if contact.user_id != current_user.id:
        flash('No tienes permiso para editar este contacto', 'danger')
        return redirect(url_for('contacts.contacts_list'))
    
    if request.method == 'POST':
        contact.name = request.form.get('name')
        contact.email = request.form.get('email')
        contact.phone = request.form.get('phone')
        contact.company = request.form.get('company')
        contact.position = request.form.get('position')
        contact.notes = request.form.get('notes')
        db.session.commit()
        flash(f'Contacto "{contact.name}" actualizado', 'success')
        return redirect(url_for('contacts.contacts_list'))
    
    return render_template('contact_form.html', contact=contact)

@contacts_bp.route('/contacts/delete/<int:id>')
@login_required
def contact_delete(id):
    """Eliminar contacto"""
    contact = Contact.query.get_or_404(id)
    
    if contact.user_id != current_user.id:
        flash('No tienes permiso para eliminar este contacto', 'danger')
    else:
        db.session.delete(contact)
        db.session.commit()
        flash(f'Contacto "{contact.name}" eliminado', 'success')
    
    return redirect(url_for('contacts.contacts_list'))