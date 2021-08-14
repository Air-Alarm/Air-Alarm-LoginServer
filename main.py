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
    conn.close()

@app.route('/signup_confirm', methods=['POST'])
def signup_confirm():
    sid_ = request.form['sid_']
    spw_ = request.form['spw_']
    spw_c = request.form['spw_c']
    semail_ = request.form['semail_']
    ssn_ = request.form['ssn_']
    if spw_ == spw_c:
        signup_db(sid_, spw_, semail_, ssn_)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('signup'))


def getPw(id):
    conn = sqlite3.connect("Test.db")
    cur = conn.cursor()
    cur.execute("SELECT pw FROM sign WHERE id='%s'" % id)
    #cur.execute(f"SELECT pw FROM sign")
    rows = cur.fetchall()
    conn.close()
    return rows[0][0]


@app.route('/login_confirm', methods=['GET', 'POST'])
def login_confirm():
    id_ = request.form['id_']
    pw_ = request.form['pw_']
    if pw_ == getPw(id_):
        session['id'] = id_
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


if __name__ == "__main__":
    app.run(debug=True)
