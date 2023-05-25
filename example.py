import json

from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages

# Это callable WSGI-приложение
app = Flask(__name__)

app.secret_key = "secret_key"


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
    all_users = json.loads(request.cookies.get('users', json.dumps([])))
    term = request.args.get('term')
    if term:
        filtered_names = list(filter(lambda name: term in name, all_users))
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
    users = json.loads(request.cookies.get('users', json.dumps([])))
    user = get_user(users, id)
    if not user:
        return 'Page not found', 404
    return render_template(
        'show.html',
        user=user,
    )


@app.post('/users')
def users_post():
    new_user = request.form.to_dict()
    errors = validate(new_user)
    if errors:
        return render_template(
            '/users/new.html',
            user=new_user,
            errors=errors,
        ), 422
    users = json.loads(request.cookies.get('users', json.dumps([])))
    next_id = json.loads(request.cookies.get('next_id', json.dumps('0')))
    user = {
        'id': next_id,
        'nickname': new_user['nickname'],
        'email': new_user['email']
    }
    next_id = str(int(next_id) + 1)
    users.append(user)
    encode_users = json.dumps(users)
    encode_id = json.dumps(next_id)
    response = redirect(url_for('get_users'))
    response.set_cookie('users', encode_users)
    response.set_cookie('next_id', encode_id)
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
    patching_user = {}
    with open('templates/users/users.json') as f:
        all_users = json.load(f)['users']

    for user in all_users:
        if user['id'] == id:
            patching_user = user
            break

    errors = []

    return render_template(
        'users/edit.html',
        user=patching_user,
        errors=errors,
    )


@app.route('/users/<id>/patch', methods=['POST'])
def patch_user(id):
    patching_user = {}
    with open('templates/users/users.json') as f:
        all_users = json.load(f)

    for user in all_users['users']:
        if user['id'] == id:
            patching_user = user
            break

    data = request.form.to_dict()

    errors = validate(data)
    if errors:
        return render_template(
            'users/edit.html',
            user=patching_user,
            errors=errors,
        ), 422

    patching_user['nickname'] = data['nickname']
    with open('templates/users/users.json', 'w') as outfile:
        outfile.write(json.dumps(all_users, indent=2))
    flash('User has been updated', 'success')
    return redirect(url_for('get_users'))


@app.route('/users/<id>/delete', methods=['POST'])
def delete_user(id):
    deleting_user = {}
    with open('templates/users/users.json') as f:
        all_users = json.load(f)

    for user in all_users['users']:
        if user['id'] == id:
            deleting_user = user
            break

    all_users['users'].remove(deleting_user)
    with open('templates/users/users.json', 'w') as outfile:
        outfile.write(json.dumps(all_users, indent=2))

    flash('User has been deleted', 'success')
    return redirect(url_for('get_users'))
