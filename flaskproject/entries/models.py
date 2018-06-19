# -*- coding: utf-8 -*-
"""
    flaskproject.entries.models
    ~~~~~~~~~~~~~~~~~~~~~~
    Entries models
"""

from ..core import db, ma
from datetime import datetime
from marshmallow import fields

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.String(300))
    category_id = db.Column(db.Integer())
    create_date = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, body, category_id, user_id, create_date=None):
        self.title = title
        self.body = body
        self.category_id = category_id
        if create_date is None:
            create_date = datetime.utcnow()
        self.create_date = create_date
        self.user_id = user_id

    def __repr__(self):
      return '<Entry %r>' % self.title


class EntryCategory(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    active = db.Column(db.Boolean(), default=True)
    name = db.Column(db.String(225))
    status_code = db.Column(db.Integer())

    def __init__(self, active, name, status_code):
        self.active = active
        self.name = name
        self.status_code = status_code

        def __repr__(self):
            return 'EntryCategory %r>' % (self.name)


class EntryCategorySchema(ma.ModelSchema):
    class Meta:
        model = EntryCategory

entry_category_schema = EntryCategorySchema()
