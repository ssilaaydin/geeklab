from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from project.models import db, Post, Comment, Like
from project.forms import CommentForm

main_routes = Blueprint('main_routes', __name__)

@main_routes.route("/")
@main_routes.route("/index")
def index():
    query = request.args.get('query')
    if query:
        posts = Post.query.filter(Post.title.contains(query) | Post.content.contains(query)).all()
    else:
        posts = Post.query.all()
    return render_template('index.html', posts=posts)

@main_routes.route("/sport")
def sport():
    posts = Post.query.filter_by(category='Sport').all()
    return render_template('category.html', posts=posts, category='Sport')

@main_routes.route("/movies")
def movies():
    posts = Post.query.filter_by(category='Movies').all()
    return render_template('category.html', posts=posts, category='Movies')

@main_routes.route("/books")
def books():
    posts = Post.query.filter_by(category='Books').all()
    return render_template('category.html', posts=posts, category='Books')

@main_routes.route("/series")
def series():
    posts = Post.query.filter_by(category='Series').all()
    return render_template('category.html', posts=posts, category='Series')

@main_routes.route("/post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('main_routes.post', post_id=post.id))
    comments = Comment.query.filter_by(post_id=post.id).all()
    return render_template('post.html', title=post.title, post=post, comments=comments, form=form)

@main_routes.route("/like/<int:post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.get_or_404(post_id)
    like = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    if like:
        db.session.delete(like)
        flash('You have unliked this post', 'success')
    else:
        like = Like(user_id=current_user.id, post_id=post.id)
        db.session.add(like)
        flash('You have liked this post', 'success')
    db.session.commit()
    return redirect(url_for('main_routes.post', post_id=post.id))
