from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from project.models import db, User, Post, Comment
from project.forms import PostForm

admin_routes = Blueprint('admin_routes', __name__)

@admin_routes.route("/admin")
@login_required
def admin():
    if not current_user.is_admin:
        flash('You do not have permission to access this page', 'danger')
        return redirect(url_for('main_routes.index'))
    users = User.query.all()
    posts = Post.query.all()
    comments = Comment.query.all()
    return render_template('admin.html', title='Admin', users=users, posts=posts, comments=comments)

@admin_routes.route("/admin/user/<int:user_id>/delete", methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash('You do not have permission to access this page', 'danger')
        return redirect(url_for('main_routes.index'))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted', 'success')
    return redirect(url_for('admin_routes.admin'))

@admin_routes.route("/admin/user/<int:user_id>/make_admin", methods=['POST'])
@login_required
def make_admin(user_id):
    if not current_user.is_admin:
        flash('You do not have permission to access this page', 'danger')
        return redirect(url_for('main_routes.index'))
    user = User.query.get_or_404(user_id)
    user.is_admin = True
    db.session.commit()
    flash('User has been promoted to admin', 'success')
    return redirect(url_for('admin_routes.admin'))

@admin_routes.route("/admin/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    if not current_user.is_admin:
        flash('You do not have permission to access this page', 'danger')
        return redirect(url_for('main_routes.index'))
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, image_url=form.image_url.data, category=form.category.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('admin_routes.admin'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@admin_routes.route("/admin/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if not current_user.is_admin:
        flash('You do not have permission to access this page', 'danger')
        return redirect(url_for('main_routes.index'))
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.image_url = form.image_url.data
        post.category = form.category.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('admin_routes.admin'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.image_url.data = post.image_url
        form.category.data = post.category
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@admin_routes.route("/admin/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if not current_user.is_admin:
        flash('You do not have permission to access this page', 'danger')
        return redirect(url_for('main_routes.index'))
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('admin_routes.admin'))
