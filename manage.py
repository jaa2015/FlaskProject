# -*- coding: utf-8 -*-
"""
    manage
    ~~~~~~
    Manager module
"""

from flask_script import Manager
from flask import json, current_app

from flaskproject import app
from flaskproject.core import db
from flaskproject.users.models import User
from flaskproject.entries.models import Entry, EntryCategory
from flaskproject.events.models import Category, Event, Status
from datetime import datetime, date
from sqlalchemy import exc

manager = Manager(app)


@manager.command
def populate():
    # Event Status
    status_active = Status(active=True, name='Active', status_code=100)
    status_inactive = Status(active=True, name='Inactive', status_code=200)
    status_cancelled = Status(active=True, name='Cancelled', status_code=300)
    status_completed = Status(active=True, name='Completed', status_code=400)
    status_archived = Status(active=True, name='Archived', status_code=500)

    # Event Categories
    category_entry_general = EntryCategory(active=True, name='General', status_code=1)
    category_entry_journal = EntryCategory(active=True, name='Journal', status_code=2)
    category_entry_log = EntryCategory(active=True, name='Log', status_code=3)

    # Event Categories
    category_event_general = Category(active=True, name='General', status_code=1)
    category_event_lunch = Category(active=True, name='Lunch', status_code=2)
    category_event_happy_hour = Category(active=True, name='Happy Hour', status_code=3)
    category_event_birthday_party = Category(active=True, name='Birthday Party', status_code=4)
    category_event_meeting = Category(active=True, name='Meeting', status_code=5)

    db.session.add(category_entry_general)
    db.session.add(category_entry_journal)
    db.session.add(category_entry_log)

    db.session.add(category_event_general)
    db.session.add(category_event_lunch)
    db.session.add(category_event_happy_hour)
    db.session.add(category_event_birthday_party)
    db.session.add(category_event_meeting)

    db.session.add(status_active)
    db.session.add(status_inactive)
    db.session.add(status_cancelled)
    db.session.add(status_completed)
    db.session.add(status_archived)

    db.session.commit()


@manager.command
def create_test_users():
    test_user = User(
        email='user@test.com',
        password='123456',
        active=True,
        birth_date=date.today(),
        last_name='Test',
        first_name='User')
    test_user2 = User(
        email='user2@test.com',
        password='123456',
        active=True,
        birth_date=date.today(),
        last_name='Test',
        first_name='User2')
    test_user3 = User(
        email='user3@test.com',
        password='123456',
        active=True,
        birth_date=date.today(),
        last_name='Test',
        first_name='User3')
    test_user4 = User(
        email='user4@test.com',
        password='123456',
        active=True,
        birth_date=date.today(),
        last_name='Test',
        first_name='User4')

    db.session.add(test_user)
    db.session.add(test_user2)
    db.session.add(test_user3)
    db.session.add(test_user4)
    db.session.commit()


## event_status_check has been automated but will remain here for reference
@manager.command
def event_status_check():
    # Check for events with status_id 100, active status.
    events = Event.query.filter_by(status_id=100).all()

    for event in events:
        # If the event end_date has expired, change its status_id
        # to 400, completed status.
        if event.end_date <= datetime.utcnow():
            event.status_id = 400

            try:
                db.session.add(event)
                print 'Success'
            except exc.SQLAlchemyError as e:
                current_app.logger.error(e)
                print 'Error'


    # Commit the db session back.
    db.session.commit()


if __name__ == "__main__":
    manager.run()
