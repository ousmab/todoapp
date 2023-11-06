from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
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
                user.password = bcrypt.hashpw(new_password.encode('utf-8') , bcrypt.gentsalt())
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

    

with app.app_context():
    db.create_all()

    result = Todo.get_all(1)
    
    print("todo all  ... ", result)

   


@app.route('/register')
def register():
    pass
    # recuperation des données
    #validation des données
    # - verification de l'emal , username, password , si le new user nexiste pas
    #sauvegarde en BD


if __name__ == "__main__":
    app.run(debug=True, port=3500)