from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from validator import validate
from helpers import hash_password
import bcrypt


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/todoAppManager.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    profil_image = db.Column(db.String(120), nullable=True)
    todos = db.relationship("Todo", backref=db.backref('user', lazy=True))


    def __repr__(self):
        return '<User %r>' % self.username

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
        user = User.get_by_email(user_email) # user / None
        if user:
            try:
                user.password = hash_password(new_password)
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
                    todos_list.append(todo)
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



####################### END POINT ####################
#######################################################


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