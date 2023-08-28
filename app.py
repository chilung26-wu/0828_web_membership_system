from flask import Flask, render_template, request, redirect, session
from bcrypt import hashpw, checkpw, gensalt

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# In a real application, you would use a database to store user data securely.
users = {'user1': 'password1'}  # Example user data (passwords should be hashed)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Hash the password before storing it
        hashed_password = hashpw(password.encode('utf-8'), gensalt())
        # Store the hashed password in the dictionary
        users[username] = hashed_password        
        return redirect('/')
    else:
        return render_template('register.html')

# @app.route('/register', methods=['POST'])
# def register():
#     username = request.form['username']
#     password = request.form['password']
#     users[username] = password  # Store the user in the dictionary (not secure)
#     return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and checkpw(password.encode('utf-8'), users[username]):
            session['username'] = username
            return redirect('/dashboard')
        else:
            return "Invalid credentials. Please try again."
    else:
        return render_template('login.html')

# @app.route('/login', methods=['POST'])
# def login():
#     username = request.form['username']
#     password = request.form['password']

#     if username in users and users[username] == password:
#         session['username'] = username
#         return redirect('/dashboard')
#     else:
#         return "Invalid credentials. Please try again."

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)