from flask import Flask, request, redirect, url_for, render_template, session, jsonify
import sqlite3
conn = sqlite3.connect("Test.db", check_same_thread=False)
cur = conn.cursor()

app = Flask(__name__, static_url_path='/static')
app.secret_key = b'_5#aby2L"F4Q8z\n\xec]'

def signup_db(id, pw, email, sn):
    #conn.execute('CREATE TABLE sign(ID TEXT, PW TEXT, EMAIL TEXT, SN TEXT)')
    cur.execute('INSERT INTO sign VALUES (?, ?, ?, ?)', (id, pw, email, sn))
    conn.commit()
    print("good", id, pw, email, sn)

@app.route('/signup_confirm', methods=['POST', 'GET'])
def signup_confirm():
    user = request.args.get('user', "user")
    pwd = request.args.get('pwd', '"pwd"')
    #pwd_c = request.args.get('pwd_c', '"pwd_c"')
    email = request.args.get('email', "email")
    SN = request.args.get('SN', "SN")
    signup_db(user, pwd, email, SN)
    temp = {"user" : user, "signup" : "True"}
    return jsonify(temp)


def getPw(id_):
    print(id_)
    cur.execute(f"SELECT pw FROM sign WHERE id={id_}")
    #cur.execute(f"SELECT pw FROM sign")
    rows = cur.fetchall()
    return rows[0][0]


@app.route('/login_confirm', methods=['GET', 'POST'])
def login_confirm():
    user = request.args.get('user', "user")
    pwd = request.args.get('pwd', '"pwd"')
    pwd = pwd.strip('"')
    print(user, pwd)
    if pwd == getPw(user):
        session['user'] = user
        temp = {"user" : user, "login" : "True"}
        return jsonify(temp)
    else:
        #return redirect(url_for('login'))
        temp = {"user" : user, "login" : "False"}
        return jsonify(temp)


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

#@app.route('/admin')
def admin():
    cur.execute("SELECT * FROM sign")
    rows = cur.fetchall()
    return rows



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=4999)

