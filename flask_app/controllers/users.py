from flask import render_template, request, redirect, flash, session
from flask_app.models import user
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_app.models import message

@app.route('/')
def index():
  if 'user_id' in session:
    return redirect("/dashboard")
  return render_template("index.html")

@app.route('/register/user', methods=['POST'])
def register():
    if not user.User.validate_user(request.form):
      return redirect('/')
    # validar el formulario aquí...
    # crear el hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # poner pw_hash en el diccionario de datos
    data = {
      "first_name": request.form['first_name'],
      "last_name": request.form['last_name'],
      "email": request.form['email'],
      "password" : pw_hash
    }
    # llama al @classmethod de guardado en Usuario
    user_id = user.User.save(data)
    # almacenar id de usuario en la sesión
    session['user_id'] = user_id
    return redirect("/dashboard")

@app.route('/login', methods=['POST'])
def login():
    # ver si el nombre de usuario proporcionado existe en la base de datos
    data = { "email" : request.form["email"] }
    user_in_db = user.User.get_user_by_email(data)
    # usuario no está registrado en la base de datos
    if not user_in_db:
      flash("Invalid Email/Password","login")
      return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
      # si obtenemos False después de verificar la contraseña
      flash("Invalid Email/Password","login")
      return redirect('/')
      # si las contraseñas coinciden, configuramos el user_id en sesión
    session['user_id'] = user_in_db.id
    # ¡¡¡Nunca renderices en una post!!!
    return redirect("/dashboard")

@app.route('/dashboard')
def dashboard():
  if 'user_id' not in session:
    return redirect("/")
  id = session["user_id"]
  messages = message.Message.get_messages_received({"id":id})
  users = user.User.get_users_except_id({"id":id})
  sent = message.Message.get_messages_sent({"id":id})
  userSession = user.User.get_user_by_id({"id":id})
  return render_template("dashboard.html",messages=messages,users=users,sent=sent,userSession=userSession)

@app.route('/logout')
def logout():
  session.clear()
  return redirect("/")
