from . import main
from flask_login import login_required, current_user
from flask import render_template,request,redirect,url_for,abort
from ..models import User, Comment, Pitch, Like, Dislike
from .forms import CommentForm, PitchForm, UpdateProfile
from .. import db, photos

@main.route('/')
def index():
    title="One minute pitches"
    return render_template('index.html', title = title)
@main.route("/pitch/general")
def pitch_general():
    general = Pitch.query.filter_by(category="General").order_by(Pitch.posted.desc()).all()
    pitches = Pitch.query.all()

    return render_template('general.html', pitches=pitches,general = general)

@main.route("/pitch/project")
def pitch_project():
    pitches = Pitch.query.all()
    project = Pitch.query.filter_by(category="Project").order_by(Pitch.posted.desc()).all()
    return render_template('project.html', pitches=pitches,project = project)

@main.route("/pitch/advertisement")
def pitch_advertisement():
    pitches = Pitch.query.all()
    advertisement = Pitch.query.filter_by(category="Advertisement").order_by(Pitch.posted.desc()).all()
    return render_template('advertisement.html', pitches=pitches,advertisement = advertisement)

@main.route("/pitch/interview")
def pitch_interview():
    pitches = Pitch.query.all()
    interview = Pitch.query.filter_by(category="Interview").order_by(Pitch.posted.desc()).all()
    return render_template('interview.html', pitches=pitches,interview= interview)

@main.route("/pitch/pickupline")
def pitch_pickupline():
    pitches = Pitch.query.all()
    pickupline = Pitch.query.filter_by(category="Pickuplines").order_by(Pitch.posted.desc()).all()
    return render_template('pickuplines.html',pitches=pitches,pickupline = pickupline)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    title = f"{uname.capitalize()}"

    if user is None:
        abort (404) 

    return render_template("profile/profile.html", user = user, title=title)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))



@main.route('/pitch/new',methods = ['GET','POST'])
@login_required
def new_pitch():
    '''
    A function that saves the pitch added
    '''
    pitch_form = PitchForm()

    if pitch_form.validate_on_submit():
        title = pitch_form.title.data
        body = pitch_form.content.data
        category = pitch_form.category.data
        title = pitch_form.title.data

        new_pitch = Pitch(title=title, content=body, category = category, user = current_user)
        new_pitch.save_pitch()

        return redirect(url_for('main.index'))


    title = 'New Pitch | One Minute Pitch'
    return render_template('newpitch.html', title = title, pitchform = pitch_form)


@main.route('/pitch/<int:pitch_id>/comment',methods = ['GET', 'POST'])
@login_required
def comment(pitch_id):
    '''
    View comments page function that returns the comment page and its data
    '''

    comment_form = CommentForm()
    pitch = Pitch.query.get(pitch_id)
    if pitch is None:
        abort(404)

    if comment_form.validate_on_submit():
        comment = comment_form.comment.data

        new_comment = Comment(comment=comment, pitch_id = pitch_id, user = current_user)
        new_comment.save_comment()

        return redirect(url_for('.comment', pitch_id=pitch_id))

    comments = Comment.query.filter_by(pitch_id=pitch_id).all()
    title = 'Comments | One Min Pitch'

    return render_template('comment.html', title = title, pitch=pitch ,comment_form = comment_form, comments = comments )





@main.route('/pitch/<int:pitch_id>/like',methods = ['GET','POST'])
def like(pitch_id):
    '''
    View like function that returns likes
    '''
    pitch = Pitch.query.get(pitch_id)

    likes = Like.query.filter_by(pitch_id=pitch_id)


    if Like.query.filter(Like.pitch_id==pitch_id).first():
        return  redirect(url_for('.index'))

    new_like = Like(pitch_id=pitch_id)
    new_like.save_likes()
    return redirect(url_for('main.index'))



@main.route('/pitch/<int:pitch_id>/dislike',methods = ['GET','POST'])
def dislike(pitch_id):
    '''
    View dislike function that returns dislikes
    '''
    pitch = Pitch.query.get(pitch_id)

    pitch_dislikes = Dislike.query.filter_by(pitch_id=pitch_id)

    if Dislike.query.filter(Dislike.pitch_id==pitch_id).first():
        return redirect(url_for('main.index'))

    new_dislike = Dislike(pitch_id=pitch_id)
    new_dislike.save_dislikes()
    return redirect(url_for('main.index')) 
