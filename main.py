from flask import Flask, request, redirect, url_for, render_template, session
import sqlite3

app = Flask(__name__, static_url_path='/static')
app.secret_key = b'_5#aby2L"F4Q8z\n\xec]'

def signup_db(id, pw, email, sn):
    conn = sqlite3.connect("Test.db")
    cur = conn.cursor()
    #conn.execute('CREATE TABLE sign(ID TEXT, PW TEXT, EMAIL TEXT, SN TEXT)')
    cur.execute('INSERT INTO sign VALUES (?, ?, ?, ?)', (id, pw, email, sn))

    conn.commit()
    #conn.close()

@app.route('/signup_confirm', methods=['POST'])
def signup_confirm():
    user = request.args.get('user', "user")
    pwd = request.args.get('pwd', '"pwd"')
    pwd_c = request.args.get('pwd_c', '"pwd_c"')
    email = request.args.get('email', 'email')
    SN = request.args.get('SN', 'SN')
    if pwd == pwd_c:
        signup_db(user, pwd, email, SN)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('signup'))


def getPw(id_):
    print(id_)
    conn = sqlite3.connect("Test.db")
    cur = conn.cursor()
    cur.execute(f"SELECT pw FROM sign WHERE id={id_}")
    #cur.execute(f"SELECT pw FROM sign")
    rows = cur.fetchall()
    #conn.close()
    return rows[0][0]


@app.route('/login_confirm', methods=['GET', 'POST'])
def login_confirm():
    user = request.args.get('user', "user")
    pwd = request.args.get('pwd', '"pwd"')
    pwd = pwd.strip('"')
    print(user, pwd)
    if pwd == getPw(user):
        session['user'] = user
        return redirect(url_for('index'))
    else:
        print("실패")
        return redirect(url_for('login'))


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


if __name__ == "__main__":
    app.run(debug=True)
