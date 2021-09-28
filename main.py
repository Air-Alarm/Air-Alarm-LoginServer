from flask import Flask, request, redirect, url_for, render_template, session, jsonify
import sqlite3
conn = sqlite3.connect("Test.db", check_same_thread=False)
cur = conn.cursor()

app = Flask(__name__, static_url_path='/static')
app.secret_key = b'_5#aby2L"F4Q8z\n\xec]'

def signup_db(id, pw, sn):
    cur.execute('INSERT INTO sign VALUES (?, ?, ?)', (id, pw, sn))
    conn.commit()
    print("good", id, pw, sn)

@app.route('/signup_confirm', methods=['POST', 'GET'])
def signup_confirm():
    id = request.args.get('id', 'id')
    pwd = request.args.get('pwd', 'pwd')
    SN = request.args.get('SN', "SN")
    if checkOverlap(id):
        temp = {"id": id, "pwd": pwd, "SN": SN , "success" : "false" }
        return jsonify(temp)
    else:
        signup_db(id, pwd, SN)
        temp = {"id": id, "pwd": pwd, "SN": SN , "success" : "true" }
        return jsonify(temp)


def getPw(id_):
    cur.execute(f'SELECT pw FROM sign WHERE id="{id_}"')
    rows = cur.fetchall()
    return rows[0][0]


def checkOverlap(id_):
    cur.execute(f'SELECT id FROM sign WHERE id="{id_}"')
    rows = cur.fetchall()
    print(rows)
    if rows:
        return True
    else:
        return False 
    

@app.route('/login_confirm', methods=['GET', 'POST'])
def login_confirm():
    id = request.args.get('id', 'id')
    pwd = request.args.get('pwd', 'pwd')
    if pwd == getPw(id):
        session['id'] = id
        temp = {"id" : id, "success" : "true"}
        return jsonify(temp)
    else:
        temp = {"id" : id, "success" : "false"}
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


@app.route('/admin')
def admin():
    cur.execute("SELECT * FROM sign")
    rows = cur.fetchall()
    return jsonify(rows)


@app.route('/remove')
def remove():
    cur.execute("DELETE FROM sign")
    return "done"


@app.route('/data')
def data():
    id = request.args.get('id', 'id')
    cur.execute(f'SELECT * FROM sign WHERE id="{id}"')
    rows = cur.fetchall()
    if rows:
        temp = {"id" : rows[0][0], "pwd" : rows[0][1], "S/N" : rows[0][2]}
        return jsonify(temp)
    else:
        return "error"

@app.route('/ip')
def ip():
    insideIp = request.args.get('inside', '127.0.0.1')
    outsideIp = request.args.get('outside', '192.168.0.1')
    SN = request.args.get('SN', 'SN')

    temp = {"inside": insideIp, "outside": outsideIp, "SN": SN}
    return jsonify(temp)

try:
    conn.execute('CREATE TABLE sign(ID TEXT, PW TEXT, SN TEXT)')
except Exception as e:
    print("already", e)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=4999)

