from flask import Flask, request, jsonify, make_response, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy 
from validator import validate
from helpers import hash_password, check_password, generate_token, check_allowed_extensions
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
import bcrypt
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/todoAppManager.db"
app.config['UPLOAD_FOLDER'] = "/static/profil/"
app.config['MAX_CONTENT_LENGTH'] = 1024*1024*3

ALLOWED_EXTENSIONS = ["jpg", "png", "jpeg","bmp","svg"]


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    profil_image = db.Column(db.String(120), nullable=True)
    todos = db.relationship("Todo", backref=db.backref('user', lazy=True))
    #is_authenticated


    
    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.username



    @staticmethod
    def update_user_by_id(user_id,username, email):
        user = User.query.get(int(user_id))
        
        try:
            user.username = username
            user.email = email
            db.session.commit()
            return True
        except Exception as e:
            print(e)
        return False

    @staticmethod
    def add(user):
        #user = User(usernmane= ,email= , pass=)
        try:
            db.session.add(user)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    
    @staticmethod
    def get(user_id):
        user = None
        try:
            user = User.query.get(int(user_id))
        except Exception as e:
            print(e)
        return user


    @staticmethod
    def get_by_username(username):
        user = None
        try:
            user = User.query.filter_by(username=username).first()
        except Exception as e :
            print(e)
        return user


    @staticmethod
    def get_by_email(email):
        user = None
        try:
            user = User.query.filter_by(email=email).first()
        except Exception as e :
            print(e)
        return user    
    
    @staticmethod
    def get_by_username_or_email(username_or_email):
        user = None
        try:
            user = User.query.filter(User.username.is_(username_or_email) | User.email.is_(username_or_email)).first()
        except Exception as e:
            print(e)
        return user
    
    @staticmethod
    def update_profil_image(user_id, new_image):
        user = User.query.get(int(user_id))
        try:
            user.profil_image = new_image
            db.session.commit()
            return True
        except Exception as e:
            print(e)
        return False
    
    @staticmethod
    def update_user_infos(user_id, data):
    # data = {email : "a@m.com"}
    # data = {'username': valeur, email: valeur ! prfo}
        user = User.query.get(int(user_id) )
        try:
            user.username = data['username'] if "username" in data.keys() else user.username 
            user.email = data['email'] if "email" in data.keys() else user.email
            user.profil_image = data['profil_image'] if "profil_image" in data.keys() else user.profil_image
            return True
        except Exception as e:
            print(e)
        return False


    @staticmethod
    def update_password(user_email, new_password):
        user = User.query.filter_by(email=user_email).first() # user / None
        if user:
            try:
                user.password = hash_password(new_password)
                db.session.commit()
                return True
            except Exception as e:
                print(e)
        return False




class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)
    archived = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "<Todo {}>".format(self.content)

    @staticmethod
    def add(todo):
        try:
            db.session.add(todo)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
        return False
    
    @staticmethod
    def get_one(todo_id, user_id):
        todo = None
        try:
            todo = Todo.query.filter(Todo.id.is_(int(todo_id)) & Todo.user_id.is_(int(user_id) ) ).first()
            if todo:
                return {
                    "id": todo.id,
                    "content": todo.content,
                    "user_owner" : todo.user_id,
                    "done" : todo.done,
                    "archived" : todo.archived,
                    "created_at" : todo.created_at,
                    "updated_at" : todo.updated_at

                }
        except Exception as e:
            print(e)
        return todo
    
    @staticmethod
    def delete_one(todo_id):
        try:
            todo = Todo.query.get( int(todo_id) )

            if todo.archived:
                return False
            db.session.delete(todo)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
        return False
    
    @staticmethod
    def update_todo_content(todo_id, new_content):
        try:
            todo = Todo.query.get(int(todo_id))
            todo.content = new_content
            todo.updated_at = db.func.now()
            db.session.commit()
            return True
        except Exception as e:
            print(e)
        return False
    
    @staticmethod
    def get_all(user_id):
        todos_list = []
        try:
            todos = Todo.query.filter_by(user_id=user_id).all()
            if todos:
                for todo in todos:
                    todo_dict = {
                        "id" : todo.id,
                        "content": todo.content,
                        "done" : todo.done,
                        "archived" : todo.archived,
                        "user_owner" : todo.user_id,
                        "created_at" : todo.created_at,
                        "updated_at" : todo.updated_at
                    }
                    todos_list.append(todo_dict)
                return todos_list
        except Exception as e :
            print(e)
        return todos_list

    @staticmethod
    def update_status_unarchived(todo_id):
        todo  = Todo.query.get(int(todo_id) )
        try:
            if todo.archived == True:
                todo.archived = False
                db.session.commit()
            return True
        except Exception as e:
            print(e)
        return False

    @staticmethod
    def update_status_archived(todo_id):
        todo = Todo.query.get(int(todo_id) )
        
        try:
            if todo.done == False:
                return False
            if todo.archived == False:
                todo.archived = True
                db.session.commit()
            return True
        except Exception as e:
            print(e)
        return False

    @staticmethod
    def update_status_do(todo_id):
        todo = Todo.query.get( int(todo_id))
        try:
            if todo.done == False:
                todo.done = True
                db.session.commit()
            return True 
        except Exception as e:
            print(e)
        return False 

    @staticmethod
    def update_status_undo(todo_id):
        todo = Todo.query.get(int(todo_id))
        try:
            if todo.done == True:
                todo.done = False
                db.session.commit()
            return True
        except Exception as e:
            print(e)
        return False

    @staticmethod
    def todo_search(keyword, user_id):
        todos = []
        try:
            todos_selected = Todo.query.filter(Todo.content.like("%"+keyword+"%") & Todo.user_id.is_(int(user_id))  ).all()
            if todos_selected:
                for todo in todos_selected:
                    todo_dict={
                        "id" : todo.id,
                        "content" : todo.content,
                        "done" : todo.done,
                        "archived" : todo.archived,
                        "user_owner" : todo.user_id,
                        "created_at" : todo.created_at,
                        "updated_at" : todo.updated_at
                    }
                    todos.append(todo_dict)
                return todos
        except Exception as e:
            print(e)
        return todos

with app.app_context():
    db.create_all()


@login_manager.unauthorized_handler
def not_connected():
    authUser = { "user":None, "username":None, "connected":False }
    return jsonify(authUser)

@app.errorhandler(413)
def handling_error(e):
    errors = {"file_size": "le fichier est trop volumineux"}
    return jsonify({"status":"error","message":"Erreur survenue lors de l'upload du fichier", "errors": errors}), 413


####################### END POINT ####################
#######################################################

@app.route("/todos", methods=['GET'])
@login_required
def get_all_todos():
    todos = Todo.get_all(current_user.id)
    print(todos)
    return jsonify({"status":"success", "data": todos})

@app.route("/todos", methods=['POST'])
@login_required
def add_todo():
    errors = {}
    content = request.json['content'].strip()
    content_check = validate({"content": content}, {"content":"required|min:3"})

    if not content_check:
        errors['content'] = "Votre tâche doit faire au moins 3 caractères"
        return jsonify({"status":"failed", "message":"Echec d'ajout", "errors": errors})

    #creer un todo
    todo = Todo(content=content, user_id=current_user.id)   
    result = Todo.add(todo)
    if result:
        return jsonify({"status":"success", "message":"Enregistrement reussie"})
    
    return jsonify({"status":'failed', "message":"Echec d'enregistrement de la tâche"})

@app.route("/profil/img/<filename>")
def get_user_image(filename):
    path_from_download = os.getcwd()+app.config['UPLOAD_FOLDER']
    try:
        return send_from_directory(path_from_download, filename)
    except Exception as e:
        print(e)
    return jsonify({"stauts":"error", "message": "Le fichier est introuvable"}), 404

@app.route("/profil/upload", methods=['POST'])
@login_required
def upload_img_profil():
    errors={}
    #recuperer les fichiers et particuliermeent le fichier user_img
    user_image = request.files['user_img']
    #securiser le fichier

    #verifier l'extention 
    result_extension_check = check_allowed_extensions(user_image.filename, ALLOWED_EXTENSIONS)['result']
    file_extension = check_allowed_extensions(user_image.filename, ALLOWED_EXTENSIONS)['extension']
    
    if not result_extension_check:
        errors['file_extension'] = "Le type de fichier n'est pas autorisé"
        return jsonify({"stauts":"failed", "message":"Extension non autorisée", "errors": errors})

    #creer un chemin de sauvegarde sur le serveur
    # C:/backend/static/profil/abou.jpg
    image_to_save  = secure_filename(current_user.username)+"."+file_extension
    #sauvegarder en BD et si cela reussi on sauvegarde sur le serveur
    save_result = User.update_profil_image(current_user.id,  image_to_save)
    if save_result:
        path = os.getcwd()+app.config['UPLOAD_FOLDER']+image_to_save
        user_image.save(path)
        return jsonify({"status":"success", "message":"Image du profil modifié avec succès"})
    return jsonify({"status":"failed", "message": "Echec de la modification de l'image du profil"})

@app.route("/profil/password-reset", methods=['PUT'])
def update_user_password():
    #recuperer les données
        #token , email , new_password
    #valider les données
        #le token doit etre de 5 caracteres , doit etre celui qui est en session
        #verifier si le password est de 8 caracteres
        #verifier que l'ancien password ne correspond pas au new_password
        #email est valide
    #si le user est connecté on s'assure que cest bien son compte qu'il modifie
    #verifier s'il ya pas d'erreurs dans le dic errors
    #modifie le password

    

    errors = {}

    
    token = request.json['token'].strip()
    new_password = request.json['new_password'].strip()
    email = request.json['email'].strip()

    user = None
    email_check = validate({"email": email}, {"email":"required|mail"})
    
    if not email_check:
        errors['email'] = "Votre mail n'est pas valide"
    else:
        user = User.get_by_email(email)
    
    if not user:
        return jsonify({"status":"failed", "message":"Echec de modification du mot de passe, Ce compte n'existe pas"})

    if current_user.is_authenticated:
        if current_user.id != user.id:
            return jsonify({"status":"failed", "message":"Vous ne pouvez pas modifier ce profil"})


    new_password_check = validate({"pass": new_password}, {"pass":"required|min:8"})
    token_check = validate({"token" : token}, {"token": "required|min:5"})
    

    if not new_password_check:
        errors['new_password'] = "le mot de passe doit faire 8 caractères"

    if not token_check:
        errors['token'] = "le format du jeton n'est pas valide"
    else:
        token_in_session = ""
        if "confirmation_token" in session:
            token_in_session = session['confirmation_token']

        if token_in_session != token:
            errors['token'] = "Mauvais jeton de confirmation veuillez consulter votre boite mail {}".format(email)
    
    if bool(errors):
        return jsonify({"status":"failed", "message":"Echec de modification du mot de passe", "errors" : errors})

   
    
    password_is_same = check_password(new_password, user.password)

    if password_is_same:
        errors['new_password'] = "Il semble que le nouveau mot de passe est le même que l'ancien"
        return jsonify({"status":"failed", "message":"Echec de modification du mot de passe", "errors": errors})

    update_password_result = User.update_password(email, new_password)
    print(update_password_result)
    if update_password_result:
        return jsonify({"status":"success", "message":"Mot de passe modifié avec succès"})
    return jsonify({"status":"failed", "message":"Echec survenue lors de la modification du mot de passe"})

@app.route("/profil/sendmail", methods=['POST'])
def send_mail():
    errors={}
    #recuperer le mail
    #verifier si le mail est valide
    #verifier si ce mail renvoi a un compte existant en DB
    #Vérifier si le user est connecté et si cest le cas alors on vérifie si cest lui qui envoi le mail
    #générer le token 5 caracteres
    #memoriser le token en session
    #envoyer le mail (on verra cette logique plutard)
    #retourner une response success

    email = request.json['email'].strip()

    email_check = validate({"email": email}, {"email":"required|mail"})
    if email_check==False:
        errors['email'] = "Veuillez renseigner un email valide !"
        return jsonify({"status":"failed", "message":"Email non valide", "errors": errors})
    
    user = User.get_by_email(email)
    if not user:
        return jsonify({"status":"failed", "message":"Ce compte n'existe pas veuillez vous inscrire !"})
    
    if current_user.is_authenticated:
        if current_user.id != user.id:
            return jsonify({"status":"failed", "message":"Vous ne pouvez pas envoyez de mail a ce compte"})
        
    token = generate_token() #a creer
    session['confirmation_token'] = token
    print(session)

    ## IMPLEMENTER LA LOGIQUE D'ENVOI DU MAIL
    #try
    #except
    ##########################################
    return jsonify({"status":"success", "message":"Consulter votre mail pour avoir le jeton de confirmation"})



@app.route("/profil/<user_id>", methods=['PUT'])
@login_required
def update_user(user_id):
    errors={}

    user = User.get(user_id)
    if not user:
        return jsonify({"status":"failed", "message":"Utilisateur non connu"})
    #on ne peut modifier que son profil (current_user.id == user_id)
    if (int(current_user.id) != int(user_id) ):
        return jsonify({"status":"failed", "message":"Vous ne pouvez pas modifier ce profil"})
    
    #recuperation des données 
    new_username = request.json['username'].strip()
    new_email = request.json['email'].strip()
    #validation des données
    new_username_check = validate({"username": new_username}, {"username":"required"})
    new_email_check = validate({"email": new_email}, {"email":"required|mail"})

    if not new_username_check:
        errors['username'] = "Veuillez renseigner un nom d'utilisateur valide"
    
    if not new_email_check:
        errors['email'] = "L'email renseigné n'est pas valide"

    if bool(errors):
        return jsonify({"status":"failed", "message":"Echec de la modification de l'utilisateur", "errors" : errors})
    #vérifie que le new email n'existe pas
   
    #vérfier que le new username n'existe pas en BD
    username_exist = None
    email_exist = None

    if new_username != user.username:
        username_exist = User.get_by_username(new_username)

    if new_email != user.email:
        email_exist = User.get_by_email(new_email)
    
    if username_exist or email_exist:
        if username_exist:
            errrors['username'] = "Le nom d'utilisateur choisi existe déjà"
        
        if email_exist:
            errors['email'] = "Cet adresse email existe déjà"
        
        return jsonify({"status":"failed", "message":"Echec de la modification de l'utilisateur", "errrors": errors})

    #effectuer la modifcation en BD
    if user.username == new_username:
        errors['username'] = "Il semble que le nom d'utilisateur est le même"
    
    if user.email == new_email:
        errors['email'] = "Il semble que l'email envoyé est le même veuillez en choisir un autre"
    
    if bool(errors):
        return jsonify({"status":"failed", "message":"Echec de la modification Choisir des données qui n'existent pas", "errors" : errors})

   
    update_result = User.update_user_by_id(user_id,new_username,new_email)
    if update_result:
        return jsonify({"status":"success", "message":"Profil utilisateur modifier avec succès"})

    return jsonify({"status":"failed", "message":"Erreur survenue lors de la modification de l'utilisateur"})

    


@app.route("/profil/<user_id>", methods=['GET'])
@login_required
def get_single_user(user_id):


    user = User.get(user_id)

    if int(current_user.id != int(user_id)):
        return jsonify({"status":"failed", "message":"Vous ne pouvez pas avoir accès à cet utilisateur"})
    if user:
        todos = []
        if user.todos:
            for todo in user.todos:
                todo_dict = {
                    "id": todo.id,
                    "content" : todo.content,
                    "done" : todo.done,
                    "archived" : todo.archived,
                    "updated_at": todo.updated_at,
                    "created_at": todo.created_at
                }
                todos.append(todo_dict)
        user_data = {
            "id": user.id,
            "email": user.email,
            "username":user.username,
            "profil_image":user.profil_image,
            "todos":todos
        }
        return jsonify({"status":"success", "message":"Utilisateur recupéré avec succès", "data":user_data })
    return jsonify({"status":"failed", "message":"Erreur lors de la récupération de l'utilisateur {}".format(user_id)})


@app.route("/authenticate", methods=["GET"])
def authenticate():
    authUser = { "user":None, "username":None, "connected":False }
    if current_user.is_authenticated:
        return jsonify({"user":current_user.id, "username":current_user.username,"connected":True, "profil_image": current_user.profil_image})
    else:
        return jsonify(authUser)


@app.route("/logout", methods=['GET'])
def logout():
    logout_user() #detruire le cookie de session
    response = make_response(jsonify({"status":"success", "message": "Deconnexion reussie"}))
    #entetes de reponses
    return response

@app.route('/login', methods=['POST'])
def login():
    # recuperation des données
   
    username_or_email = request.json['username'].strip()
    password = request.json['password'].strip()
    remember = request.json['remember']
    #valider les données
    username_or_email_check = validate({"username": username_or_email}, {"username": "required"})
    password_check = validate({"pass": password}, {"pass": "required"})


    if not username_or_email_check or not password_check:
        return jsonify({"status":"failed", "message":"Veuillez renseigner un couple username ou email / et mot de passe valide"})
    #verifier la presence l'utilisateur ne BD a partir du username

    user = User.get_by_username_or_email(username_or_email)
    user_password_check = False
    if user:
        user_password_check = check_password(password, user.password)
    else:
        return jsonify({"status":"failed", "message":"Le couple username ou email / mot de passe est incorrect"})
    
    if user and user_password_check:
        #on logge l'utilisateur et flask-login au travers de la methode login_user creer les cookie de session et le cookie 
        #remember me
        login_user(user, remember= remember | False) 
        authUser = { "user":user.id, "username":user.username, "connected":True }
        return jsonify({"status":"success", "message":"Connexion reussie", "data": authUser})
    else:
        return jsonify({"status":"failed", "message":"Le couple username ou email / mot de passe est incorrect"})

    #si l'utilisateur existe et si le mot de passe correspond au mot de passe hashé (bcryt.checkpw(pass, pwhasse) )
    #si l'utilisateur existe et le mot de passe est correct : on va le connecter ( en utilisant flask-login)
    #retourner les informations du user connecté




@app.route('/register', methods=['POST'])
def register():
    
    # recuperation des données
    username = request.json['username'].strip()
    email = request.json['email'].strip()
    password = request.json['password'].strip()
    errors={}

    # validation
    username_check =  validate({"username" : username} , {"username" : "required"}  )
    email_check =  validate({"mail" : email} , {"mail" : "required|mail"}  )
    password_check =  validate({"pass" : password} , {"pass" : "required|min:8"}  )

    if username_check==False:
        errors['username'] = "Veuillez renseigner un nom d'utilisateur !"
    else:
        user = User.get_by_username(username)
        if user:
            errors['username'] = "Cet utilisateur existe déjà !"

    if email_check==False:
        errors['email'] = "Veuillez renseigner un email valide !"
    else:
        user = User.get_by_email(email)
        if user:
            errors['email'] = "Cet email est déjà enregistré !"

    if password_check==False:
        errors['password'] = "Le mot de passe doit faire au moins 8 caractères"
    
    if bool(errors):
        return jsonify({"status":"failed", "message": "echec de l'inscription", "errors" : errors })
    else:
        #hasher le mot de passe
        password_hashed = hash_password(password)
        user = User(email=email, password=password_hashed, username=username)
        save_result = User.add(user)

        if save_result:
            return jsonify({"status":"success", "message": "l'utilisateur {} est inscrit avec succès".format(username)})
    
    return jsonify({"status":"failed", "message":" echec de l'inscription erreur non connu"}), 400

 


if __name__ == "__main__":
    app.run(debug=True, port=3500)