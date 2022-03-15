from flask import Flask, render_template, request, session, redirect
from flask_mongoengine import MongoEngine
from flask_session import Session
from modules.PasswordGenerator import PasswordGenerator

app = Flask(
    __name__,
    static_url_path='',
    static_folder='static',
    template_folder='templates',
)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['MONGODB_SETTINGS'] = {
    'db': 'password_manager',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine(app)

# Database


class NewUser(db.Document):
    name = db.StringField()
    email = db.StringField()
    username = db.StringField()
    password = db.StringField()

    def to_json(self):
        return {
            'name': self.name,
            'email': self.email,
            'username': self.username,
            'password': self.password,
        }


class Passwords(db.Document):
    user = db.StringField()
    website = db.StringField()
    username = db.StringField()
    password = db.StringField()

    def to_json(self):
        return {
            "website": self.website,
            "username": self.username,
            "password": self.password,
        }

# Server


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html', error_message='')


@app.route('/login.py', methods=['POST', 'GET'])
def login_user():
    try:
        user = NewUser.objects(
            username=request.form['login--username'], password=request.form['login--password']).first()
        if not user:
            return render_template('login.html', error_message="Invalid username or password")

        # Create Session
        session['username'] = request.form['login--username']
        # Get name from db
        name = NewUser\
            .objects(username=session['username'])\
            .get()\
            .to_json()['name']
        # Redirect to Dashboard
        return render_template('/main.html', user=name, username=session['username'])
    except:
        return redirect('/')


@app.route('/register')
def register():
    return render_template('register.html', error_message='')


@app.route('/register.py', methods=['POST'])
def register_user():
    user = NewUser.objects(username=request.form['register--username'])
    if user:
        return render_template("register.html", error_message="Username already exists")
    else:
        print(user)
        new_user = NewUser(
            name=request.form['register--name'],
            email=request.form['register--email'],
            username=request.form['register--username'],
            password=request.form['register--password'],
        )
        new_user.save()
        return render_template('login.html')


@app.route('/gen_pass')
def generate_password():
    PSWD = PasswordGenerator()
    return {"password": f'{PSWD.get_password()}'}


@app.route('/save_pass', methods=['POST'])
def save_password():
    # Handle Same username for same website
    data = request.get_json()
    password = Passwords.objects(
        user=session['username'], website=data['website'], username=data['username']).first()
    if password:
        return {"message": "Exists"}
    new_pass = Passwords(
        user=data['user'],
        website=data['website'],
        username=data['username'],
        password=data['password'],
    )
    new_pass.save()
    return {'message': 'Saved'}, 200


@app.route('/get_pass', methods=['GET'])
def get_password():
    if not session['username']:
        return redirect('/')
    passwords = Passwords.objects(user=session['username']).filter()
    data = []
    for password in passwords:
        password = password.to_json()
        data.append(password)
    return {"passwords": data}, 200


@app.route('/search_pass', methods=['POST'])
def search_password():
    if not session['username']:
        redirect('/')
    data = request.get_json()
    passwords = Passwords.objects(
        user=data['username'],
        website=data['website']
    ).filter()
    data = []
    for password in passwords:
        password.to_json()
        data.append(password)
    return {"passwords": data}, 200


@app.route('/del_pass', methods=['POST'])
def delete_password():
    if not session['username']:
        redirect('/')
    data = request.get_json()
    password = Passwords.objects(
        user=session['username'],
        website=data['website'],
        username=data['username']
    ).first()
    password.delete()
    return {"message": "OK"}, 200


@app.route('/logout.py')
def logout():
    session['username'] = None
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
