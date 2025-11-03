from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__, static_folder='static', template_folder='.')

users_db = []

@app.route('/')
def index():
    """Serve the main HTML page with modal state"""
    show_modal = request.args.get('modal') == 'open'
    active_tab = request.args.get('tab', 'signup')
    
    return render_template('index.html', 
                         show_modal=show_modal, 
                         active_tab=active_tab,
                         error=None,
                         success=None)

@app.route('/login', methods=['POST'])
def login():
    """Handle login form submission"""
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email or not password:
        return render_template('index.html',
                             show_modal=True,
                             active_tab='login',
                             error='Email e senha são obrigatórios',
                             success=None)
    
    user = next((u for u in users_db if u['email'] == email), None)
    
    if user and user.get('password') == password:
        return render_template('index.html',
                             show_modal=True,
                             active_tab='login',
                             error=None,
                             success=f'Bem-vindo de volta, {user["firstName"]}!')
    else:
        return render_template('index.html',
                             show_modal=True,
                             active_tab='login',
                             error='Email ou senha incorretos',
                             success=None)

@app.route('/signup', methods=['POST'])
def signup():
    """Handle signup form submission"""
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not all([first_name, last_name, email, password]):
        return render_template('index.html',
                             show_modal=True,
                             active_tab='signup',
                             error='Todos os campos são obrigatórios',
                             success=None)
    
    if any(u['email'] == email for u in users_db):
        return render_template('index.html',
                             show_modal=True,
                             active_tab='signup',
                             error='Email já cadastrado',
                             success=None)
    
    new_user = {
        'firstName': first_name,
        'lastName': last_name,
        'email': email,
        'password': password  # In production, hash this!
    }
    users_db.append(new_user)
    
    return render_template('index.html',
                         show_modal=True,
                         active_tab='signup',
                         error=None,
                         success=f'Cadastro realizado com sucesso! Bem-vindo, {first_name}!')

@app.route('/auth/google')
def google_auth():
    """Handle Google authentication (placeholder)"""
    return render_template('index.html',
                         show_modal=True,
                         active_tab='signup',
                         error=None,
                         success='Autenticação com Google em desenvolvimento')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
