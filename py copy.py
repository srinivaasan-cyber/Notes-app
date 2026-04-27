from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(20), nullable=False)

db.create_all()

def index():
    notes = Note.query.all()
    return render_template('index.html', notes=notes)


def add_note():
    title = request.form['title']
    description = request.form['description']

    if title or description:
        current_date = datetime.now()
        month = months[current_date.month]
        day = current_date.day
        year = current_date.year

        note = Note(title=title, description=description, date=f'{month} {day}, {year}')
        db.session.add(note)
        db.session.commit()

    return redirect(url_for('index'))


def delete_note(note_id):
    note = Note.query.get(note_id)
    if note:
        db.session.delete(note)
        db.session.commit()
    return redirect(url_for('index'))


def update_note(note_id):
    note = Note.query.get(note_id)
    return render_template('update.html', note=note, note_id=note_id)

def perform_update(note_id):
    note = Note.query.get(note_id)
    if note:
        note.title = request.form['title']
        note.description = request.form['description']
        db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

