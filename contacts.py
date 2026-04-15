from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import uuid
from models import db, Contact

# Crear blueprint para contactos
contacts_bp = Blueprint('contacts', __name__)

ALLOWED_IMAGE_EXTENSIONS = {'png'}


def _allowed_image_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def _save_contact_photo(photo_file):
    """Guardar imagen de contacto en static/uploads/contacts y devolver ruta relativa."""
    if not photo_file or photo_file.filename == '':
        return None

    filename = secure_filename(photo_file.filename)
    if not _allowed_image_file(filename):
        return None

    extension = filename.rsplit('.', 1)[1].lower()
    new_filename = f"{uuid.uuid4().hex}.{extension}"
    upload_dir = os.path.join(contacts_bp.root_path, 'static', 'uploads', 'contacts')
    os.makedirs(upload_dir, exist_ok=True)
    photo_file.save(os.path.join(upload_dir, new_filename))
    return f"uploads/contacts/{new_filename}"


def _delete_contact_photo(photo_path):
    """Eliminar archivo de foto si pertenece al directorio permitido."""
    if not photo_path or not photo_path.startswith('uploads/contacts/'):
        return

    absolute_path = os.path.join(contacts_bp.root_path, 'static', photo_path)
    if os.path.exists(absolute_path):
        os.remove(absolute_path)

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
        photo_file = request.files.get('photo')
        photo_path = _save_contact_photo(photo_file)

        if photo_file and photo_file.filename and not photo_path:
            flash('Solo se permiten imagenes PNG para el icono del contacto', 'danger')
            return render_template('contact_form.html', contact=None)

        contact = Contact(
            name=request.form.get('name'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            photo=photo_path,
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
        remove_photo_requested = request.form.get('remove_photo') == '1'
        if remove_photo_requested and contact.photo:
            _delete_contact_photo(contact.photo)
            contact.photo = None

        photo_file = request.files.get('photo')
        if photo_file and photo_file.filename:
            photo_path = _save_contact_photo(photo_file)
            if not photo_path:
                flash('Solo se permiten imagenes PNG para el icono del contacto', 'danger')
                return render_template('contact_form.html', contact=contact)

            if contact.photo:
                _delete_contact_photo(contact.photo)
            contact.photo = photo_path

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