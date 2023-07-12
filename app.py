from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    noteName = db.Column(db.String(100), nullable=False)
    note = db.Column(db.Text, nullable=True)
    #userUd = db.Column(db.Int, nullable=False, foreign_key=True)
    createdDate = db.Column(db.DateTime, default=datetime.utcnow)
    editedDate = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Note %r' % self.id


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/notes')
def notes():
    notes = Note.query.order_by(Note.createdDate.desc()).all()
    return render_template('notes.html', notes=notes)


@app.route('/notes/<int:id>')
def note_detail(id):
    note = Note.query.get(id)
    return render_template('note.html', note=note)


@app.route('/notes/<int:id>/delete')
def note_delete(id):
    note = Note.query.get_or_404(id)

    try:
        db.session.delete(note)
        db.session.commit()
        return redirect('/notes')
    except:
        'При удалении возникла ошибка'


@app.route('/notes/<int:id>/update', methods=['POST', 'GET'])
def note_update(id):
    note = Note.query.get(id)
    if request.method == 'POST':
        note.noteName = request.form['noteName']
        note.note = request.form['note']
        note.editedDate = datetime.utcnow()

        try:
            db.session.commit()
            return redirect('/notes')
        except:
            'При создании заметки произошла ошибка'
    else:
        return render_template('note-update.html', note=note)


@app.route('/notes/create', methods=['POST', 'GET'])
def create_note():
    if request.method == 'POST':
        noteName = request.form['noteName']
        note = request.form['note']

        note_obj = Note(noteName=noteName, note=note)

        try:
            db.session.add(note_obj)
            db.session.commit()
            return redirect('/notes')
        except:
            'При создании заметки произошла ошибка'
    else:
        return render_template('note-create.html')


if __name__ == '__main__':
    app.run(debug=True)