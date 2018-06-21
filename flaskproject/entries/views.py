from flask import Blueprint, render_template
from flask import request, redirect, url_for, json, current_app
from ..core import db
from flask_security import login_required, current_user
from datetime import datetime
from .forms import CreateEntryForm, UpdateEntryForm
from .models import Entry, EntryCategory
from sqlalchemy import exc

entries = Blueprint('entries', __name__, template_folder='templates')

@entries.route('/')
@login_required
def index():
    user_id = current_user.id
    entries = Entry.query.filter_by(user_id=user_id)

    return render_template('entries/entries.html', entries=entries)

@entries.route('/')
@login_required
def display_entries():
    user_id = current_user.id
    entries = Entry.query.filter_by(user_id=user_id)

    return render_template("entries/entries.html", entries=entries)

@entries.route('/create', methods=['GET', 'POST'])
@login_required
def create_entry():
    form = CreateEntryForm(request.form)

    form.category_id.choices = [(ec.status_code, ec.name) for ec in EntryCategory.query.order_by('name')]

    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        # category_id = 1
        category_id = form.category_id.data
        user_id = current_user.id
        entry = Entry(title, body, category_id, user_id)

        try:
            db.session.add(entry)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            current_app.logger.error(e)


        return redirect(url_for('entries.display_entries'))

    return render_template("entries/create_entry.html", form=form)

@entries.route('/<entry_id>', methods=['GET', 'POST'])
@login_required
def show(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    print(entry.category_id)

    return render_template("entries/show.html", entry=entry)

@entries.route('/edit/<entry_id>', methods=['GET', 'POST'])
@login_required
def update(entry_id):
    form = UpdateEntryForm()
    entry = Entry.query.filter_by(id=entry_id).first_or_404()

    form.category_id.choices = [(ec.status_code, ec.name) for ec in EntryCategory.query.order_by('name')]

    if request.method == "POST" and form.validate_on_submit():
        entry.body = form.body.data
        entry.category_id = form.category_id.data
        entry.title = form.title.data

        try:
            db.session.commit()
        except exc.SQLAlchemyError as e:
            current_app.logger.error(e)

        return redirect(url_for('entries.show', entry_id=entry.id))
    else:
        form.body.data = entry.body
        form.category_id.data = entry.category_id
        form.title.data = entry.title

    return render_template("entries/edit.html", entry=entry, form=form)

@entries.route('/delete/<entry_id>', methods=['GET', 'POST'])
@login_required
def delete(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    user_id = current_user.id
    if user_id == entry.user_id:
        try:
            db.session.delete(entry)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            current_app.logger.error(e)

        return redirect(url_for('entries.display_entries'))

    return redirect(url_for('entries.display_entries'))

