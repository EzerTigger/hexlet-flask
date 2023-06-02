import os
from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, session

# Это callable WSGI-приложение
app = Flask(__name__)

app.config['SECRET_KEY'] = 'b722f75d2433fac5e59a481a7dbc387f181bc730'


def get_user(arr, id):
    for user in arr:
        if user['id'] == id:
            return user


def validate(user):
    errors = {}

    if len(user['nickname']) < 4:
        errors['nickname'] = 'Имя должно быть длиннее 3 символов'

    return errors


@app.route('/users')
def get_users():
    all_users = session['users']
    term = request.args.get('term')
    if term:
        filtered_names = list(
            filter(lambda name: term in name['nickname'], all_users))
        users = filtered_names
    else:
        users = all_users

    messages = get_flashed_messages(with_categories=True)

    return render_template('users/index.html',
                           users=users,
                           messages=messages
                           )


@app.route('/users/<id>')
def user_page(id):
    users = session['users']
    user = get_user(users, id)
    if not user:
        return 'Page not found', 404
    return render_template(
        'show.html',
        user=user,
    )


@app.post('/users')
def users_post():
    if session.get('users') is None:
        session['users'] = []
    if session.get('next_id') is None:
        session['next_id'] = '0'
    new_user = request.form.to_dict()
    if new_user.get('nickname') is None:
        if session['users']:
            for user in session['users']:
                if user['email'] == new_user['email']:
                    response = redirect(url_for('get_users'))
                    return response
            return render_template(
                '/users/auth.html',
                errors={'email': 'Нет такого пользователя'}
            ), 422
    errors = validate(new_user)
    if errors:
        return render_template(
            '/users/new.html',
            user=new_user,
            errors=errors,
        ), 422

    users = session['users']
    next_id = session['next_id']
    user = {
        'id': next_id,
        'nickname': new_user['nickname'],
        'email': new_user['email']
    }
    session['next_id'] = str(int(next_id) + 1)
    users.append(user)
    response = redirect(url_for('get_users'))
    flash('User was added successfully', 'success')
    return response


@app.route('/users/new')
def new_user():
    user = []
    errors = []
    return render_template(
        '/users/new.html',
        user=user,
        errors=errors,
    )


@app.route('/users/<id>/edit')
def edit_user(id):
    users = session['users']
    patching_user = get_user(users, id)
    errors = []
    return render_template(
        'users/edit.html',
        user=patching_user,
        errors=errors,
    )


@app.route('/users/<id>/patch', methods=['POST'])
def patch_user(id):
    users = session['users']
    patching_user = get_user(users, id)
    data = request.form.to_dict()
    errors = validate(data)
    if errors:
        return render_template(
            'users/edit.html',
            user=patching_user,
            errors=errors,
        ), 422

    patching_user['nickname'] = data['nickname']
    response = redirect(url_for('get_users'))
    flash('User has been updated', 'success')
    return response


@app.route('/users/<id>/delete', methods=['POST'])
def delete_user(id):
    users = session['users']
    deleting_user = get_user(users, id)
    users.remove(deleting_user)
    response = redirect(url_for('get_users'))
    flash('User has been deleted', 'success')
    return response


@app.route('/')
def login_user():
    user = []
    errors = []
    return render_template(
        '/users/auth.html',
        user=user,
        errors=errors
    )


if __name__ == '__main__':
    app.run()
