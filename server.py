import re, sys
from flask import Flask, session, request, redirect, render_template, flash, url_for

import db.data_layer as db

from db.data_layer import get_all_quotes, get_all_quotes_for, search_by_user_or_email, create_quote, delete_quote, get_user_by_id, get_user_by_name, get_user_by_email, create_user

# '''
# USAGE:        db.<function_name>
# EXAMPLES:     db.search_by_user_or_email('Smith')
#               db.search_by_user_or_email('gmail.com')
# '''

EMAIL_REGEX = re.compile(r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$')

app = Flask(__name__)
app.secret_key = '0d599f0ec05c3bda8c3b8a68c32a1b47'

@app.route('/')
def index():
    return render_template('index.html', quotes = get_all_quotes())

@app.route('/create_quote', methods=['POST'])
def post_quote():
    if 'user_id' in session:
        content = request.form['content']
        create_quote(session['user_id'], content)
    return redirect(url_for('index'))

@app.route('/delete/<quote_id>')
def destroy_quote(quote_id):
    delete_quote(quote_id)
    return redirect(url_for('index'))

@app.route('/search')
def search():
    print(request.args['html_query'])
    print('--------------------------------------------------------')
    sys.stdout.flush()
    return redirect(url_for('search_users', query=request.args['html_query']))
    
@app.route('/results/<query>')
def search_users(query):
    users = search_by_user_or_email(query)
    return render_template('user/search_user.html', users = users, query = query)

@app.route('/user/<user_id>')
def user_quotes(user_id):
    return render_template('user/quote.html', quotes = get_all_quotes_for(user_id))

def is_blank(name, field):
    if len(name) == 0:
        flash('{} cannot be blank'.format(name))
        return True
    return False

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['html_email'] 
        password = request.form['html_password']
        try:
            user = get_user_by_email(email)
            if user.password == password:
                setup_web_session(user)
                return redirect(url_for('index'))
            else:
                flash('Password not match')
        except:
            raise
            flash('Login failed')
        return redirect(url_for('authenticate'))
    else:
        return render_template('user/login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    print('--------------------------------------------------')
    print(request.method)
    if request.method == 'POST':
        fullname = request.form['html_fullname']
        email = request.form['html_email']
        password = request.form['html_password']
        confirm = request.form['html_confirm']

        is_valid = True

        is_valid = not is_blank('Fullname', fullname)
        is_valid = not is_blank('Email', email)
        is_valid = not is_blank('Password', password)
        is_valid = not is_blank('Confirm Password', confirm)

        if password != confirm:
            flash('Password do not match')
            is_valid = False
        if len(password) < 6:
            flash('Password have to be more than 6')
            is_valid = False
        if not EMAIL_REGEX.match(email):
            flash('Email format is wrong')
            is_valid = False

        if is_valid:
            try:
                user = create_user(email, fullname, password)
                setup_web_session(user)
                return redirect(url_for('index'))
            except:
                flash('Email alredy registered')
        return redirect(url_for('register'))
    else:
        return render_template('user/register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def setup_web_session(user):
    session['user_id'] = user.id
    session['user_name'] = user.email
    session['name'] = user.name


app.run(debug=True)
