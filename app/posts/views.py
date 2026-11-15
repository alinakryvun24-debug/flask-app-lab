from flask import (
    render_template, redirect, url_for,
    flash, session, request
)

from app import db
from . import post_bp
from .models import Post
from .forms import PostForm, DeletePostForm


# Список активних постів
@post_bp.route('')
@post_bp.route('/')
def all_posts():
    statement = (
        db.select(Post)
        .where(Post.is_active.is_(True))
        .order_by(Post.posted.desc(), Post.id.desc())
    )

    posts = db.session.scalars(statement).all()

    return render_template(
        'posts/all_posts.html',
        title='Пости',
        posts=posts
    )


# Створення поста
@post_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.enabled.data,
            posted=form.publish_date.data,
            category=form.category.data,
            author=session.get('username', 'Anonymous')
        )

        db.session.add(post)
        db.session.commit()

        flash('Пост успішно створено!', 'success')
        return redirect(url_for('posts.detail_post', id=post.id))

    return render_template(
        'posts/add_post.html',
        title='Додавання поста',
        form=form
    )


# Перегляд одного поста
@post_bp.route('/<int:id>')
def detail_post(id):
    post = db.get_or_404(Post, id)

    return render_template(
        'posts/detail_post.html',
        title=post.title,
        post=post
    )


# Редагування поста
@post_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)

    # Ці поля форми мають інші назви, ніж поля моделі
    if request.method == 'GET':
        form.enabled.data = post.is_active
        form.publish_date.data = post.posted

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.enabled.data
        post.posted = form.publish_date.data
        post.category = form.category.data

        db.session.commit()

        flash('Пост успішно оновлено!', 'success')
        return redirect(url_for('posts.detail_post', id=post.id))

    return render_template(
        'posts/add_post.html',
        title='Редагування поста',
        form=form
    )


# Підтвердження та видалення поста
@post_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    post = db.get_or_404(Post, id)
    form = DeletePostForm()

    if form.validate_on_submit():
        db.session.delete(post)
        db.session.commit()

        flash('Пост успішно видалено!', 'success')
        return redirect(url_for('posts.all_posts'))

    return render_template(
        'posts/delete_confirm.html',
        title='Видалення поста',
        post=post,
        form=form
    )