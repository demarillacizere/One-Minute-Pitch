from . import main
from flask_login import login_required, current_user
from flask import render_template,request,redirect,url_for,abort
from ..models import User, Comment, Pitch, Like, Dislike
from .forms import CommentForm, PitchForm, UpdateProfile
from .. import db, photos

@main.route('/')
def index():
    form = PitchForm()
    general = Pitch.query.filter_by(category="general").order_by(Pitch.posted.desc()).all()
    project = Pitch.query.filter_by(category="project").order_by(Pitch.posted.desc()).all()
    advertisement = Pitch.query.filter_by(category="advertisement").order_by(Pitch.posted.desc()).all()
    sale = Pitch.query.filter_by(category="sale").order_by(Pitch.posted.desc()).all()

    pitch = Pitch.query.filter_by().first()
    likes = Like.get_all_likes(pitch_id=Pitch.id)
    dislikes = Dislike.get_all_dislikes(pitch_id=Pitch.id)
    title="One minute pitches"
    return render_template('index.html', pitchform=form, title = title, pitch = pitch, general = general, project = project, advertisement = advertisement, sale = sale, likes=likes, dislikes=dislikes)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    title = f"{uname.capitalize()}"

    get_pitches = Pitch.query.filter_by(user_id = User.id).all()
    get_comments = Comment.query.filter_by(user_id = User.id).all()
    get_likes = Like.query.filter_by(user_id = User.id).all()
    get_dislikes = Dislike.query.filter_by(user_id = User.id).all()

    if user is None:
        abort (404) 

    return render_template("profile/profile.html", user = user, title=title, pitches_no = get_pitches, comments_no = get_comments, likes_no = get_likes, dislikes_no = get_dislikes)

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

        new_pitch = Pitch(title=title, content=body, category = category, user = current_user,likes=0,dislikes=0)
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
        comment_body = comment_form.comment.data

        new_comment = Comment(comment=comment_body, pitch_id = pitch_id, user = current_user)
        new_comment.save_comment()

        return redirect(url_for('.comment', pitch_id=pitch_id))

    comments = Comment.query.filter_by(pitch_id=pitch_id).all()
    title = 'New Comment | One Min Pitch'

    return render_template('comment.html', title = title, pitch=pitch ,comment_form = comment_form, comment = comments )





@main.route('/pitch/<int:pitch_id>/like',methods = ['GET','POST'])
@login_required
def like(pitch_id):
    '''
    View like function that returns likes
    '''
    pitch = Pitch.query.get(pitch_id)
    user = current_user

    likes = Like.query.filter_by(pitch_id=pitch_id)


    if Like.query.filter(Like.user_id==user.id,Like.pitch_id==pitch_id).first():
        return  redirect(url_for('.index'))

    new_like = Like(pitch_id=pitch_id, user = current_user)
    new_like.save_likes()
    return redirect(url_for('.index'))



@main.route('/pitch/<int:pitch_id>/dislike',methods = ['GET','POST'])
@login_required
def dislike(pitch_id):
    '''
    View dislike function that returns dislikes
    '''
    pitch = Pitch.query.get(pitch_id)
    user = current_user

    pitch_dislikes = Dislike.query.filter_by(pitch_id=pitch_id)

    if Dislike.query.filter(Dislike.user_id==user.id,Dislike.pitch_id==pitch_id).first():
        return redirect(url_for('.index'))

    new_dislike = Dislike(pitch_id=pitch_id, user = current_user)
    new_dislike.save_dislikes()
    return redirect(url_for('.index'))



@main.route('/user/category/advertisement', methods=['GET', 'POST'])
@login_required
def advertisement():
    form = AdvertisementForm()
    title = 'Post a pitch'
    if form.validate_on_submit():
        post = form.post.data
        body = form.body.data
        new_advertisement = Advertisement(post=post, user=current_user, body=body)
        new_advertisement.save_advertisement()
        return redirect(url_for('.advertisements'))
    return render_template("advertisement.html", advertisement_form=form, title=title)

@main.route('/')   
def pitches(category):
    