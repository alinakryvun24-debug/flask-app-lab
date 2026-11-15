
from flask import (
    render_template, request, url_for, redirect,
    flash, session, make_response, current_app
)

from . import users_bp


@users_bp.route('/hi/<string:name>')
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, type=int)
    return render_template("users/hi.html", name=name, age=age)


@users_bp.route('/admin')
def admin():
    to_url = url_for(
        "users.greetings",
        name="administrator",
        age=45,
        _external=True
    )
    return redirect(to_url)


# Сторінка входу
@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == '12345':
            session['username'] = username
            flash('Ви успішно увійшли в систему!', 'success')
            return redirect(url_for('users.profile'))
        else:
            flash('Неправильний логін або пароль!', 'error')
            return redirect(url_for('users.login'))

    return render_template('login.html', title='Вхід')


# Сторінка профілю
@users_bp.route('/profile')
def profile():
    if 'username' not in session:
        flash('Спочатку потрібно увійти в систему!', 'error')
        return redirect(url_for('users.login'))

    # Отримуємо cookies, крім службової cookie сесії Flask
    session_cookie = current_app.config.get('SESSION_COOKIE_NAME', 'session')
    cookies = [
        (key, value)
        for key, value in request.cookies.items()
        if key != session_cookie
    ]

    theme = request.cookies.get('profile_theme', 'light')

    return render_template(
        'profile.html',
        title='Профіль',
        username=session['username'],
        cookies=cookies,
        theme=theme
    )


# Додавання cookie
@users_bp.route('/cookies/add', methods=['POST'])
def add_cookie():
    if 'username' not in session:
        flash('Спочатку потрібно увійти в систему!', 'error')
        return redirect(url_for('users.login'))

    key = request.form.get('key', '').strip()
    value = request.form.get('value', '')
    max_age = request.form.get('max_age', type=int)

    session_cookie = current_app.config.get('SESSION_COOKIE_NAME', 'session')

    if not key or max_age is None or max_age <= 0:
        flash('Введіть ключ і правильний термін дії cookie!', 'error')
        return redirect(url_for('users.profile'))

    if key == session_cookie:
        flash('Цей ключ зарезервований для системної сесії!', 'error')
        return redirect(url_for('users.profile'))

    response = make_response(redirect(url_for('users.profile')))
    response.set_cookie(key, value, max_age=max_age)
    flash('Cookie успішно додано!', 'success')
    return response


# Видалення однієї cookie
@users_bp.route('/cookies/delete', methods=['POST'])
def delete_cookie():
    if 'username' not in session:
        flash('Спочатку потрібно увійти в систему!', 'error')
        return redirect(url_for('users.login'))

    key = request.form.get('key', '').strip()

    if not key:
        flash('Введіть ключ cookie для видалення!', 'error')
        return redirect(url_for('users.profile'))

    response = make_response(redirect(url_for('users.profile')))
    response.delete_cookie(key)
    flash('Cookie успішно видалено!', 'success')
    return response


# Видалення всіх cookies, крім службової cookie сесії Flask
@users_bp.route('/cookies/delete-all', methods=['POST'])
def delete_all_cookies():
    if 'username' not in session:
        flash('Спочатку потрібно увійти в систему!', 'error')
        return redirect(url_for('users.login'))

    response = make_response(redirect(url_for('users.profile')))
    session_cookie = current_app.config.get('SESSION_COOKIE_NAME', 'session')

    for key in request.cookies:
        if key != session_cookie:
            response.delete_cookie(key)

    flash('Усі користувацькі cookies успішно видалено!', 'success')
    return response


# Зміна кольорової схеми профілю
@users_bp.route('/profile/theme', methods=['POST'])
def change_theme():
    if 'username' not in session:
        flash('Спочатку потрібно увійти в систему!', 'error')
        return redirect(url_for('users.login'))

    theme = request.form.get('theme')

    if theme not in ['light', 'dark']:
        flash('Невідома кольорова схема!', 'error')
        return redirect(url_for('users.profile'))

    response = make_response(redirect(url_for('users.profile')))
    response.set_cookie('profile_theme', theme, max_age=31536000)

    return response


# Вихід із системи
@users_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    flash('Ви вийшли із системи.', 'info')
    return redirect(url_for('users.login'))
