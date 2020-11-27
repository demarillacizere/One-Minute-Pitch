from flask import render_template
from . import main
from flask_login import login_required

@main.route('/')
def index():
    title="One minute pitches"
    return render_template('index.html', title = title)

@main.route('/pitch/comment/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_comment(id):
    pass