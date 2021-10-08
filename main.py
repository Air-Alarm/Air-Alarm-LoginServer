from flask import Flask, request, redirect, url_for, render_template, session, jsonify
import sqlite3
conn = sqlite3.connect("Test.db", check_same_thread=False)
cur = conn.cursor()

app = Flask(__name__, static_url_path='/static')
app.secret_key = b'_5#aby2L"F4Q8z\n\xec]'

# 데이터베이스에 회원가입 데이터를 넣는 메소드
def signup_db(id, pw, sn):
    cur.execute('INSERT INTO sign VALUES (?, ?, ?)', (id, pw, sn))
    conn.commit()
    print("good", id, pw, sn)

# 앱으로부터 회원가입 데이터를 전달받는 메소드
@app.route('/signup_confirm', methods=['POST', 'GET'])
def signup_confirm():
    # id, pwd, SN을 url을 통해 받아냄.
    id = request.args.get('id', 'id')
    pwd = request.args.get('pwd', 'pwd')
    SN = request.args.get('SN', "SN")
    if checkOverlap(id): # 중복된 id가 있는지 체크
        temp = {"id": id, "pwd": pwd, "SN": SN , "success" : "false" }
        return jsonify(temp) # 중복될 시 false 반환
    else:
        signup_db(id, pwd, SN)
        temp = {"id": id, "pwd": pwd, "SN": SN , "success" : "true" }
        return jsonify(temp) # 중복 아니면 ture 반환

# id를 매개변수로 받아 id에 해당하는 비밀번호를 반환하는 함수
def getPw(id_):
    cur.execute(f'SELECT pw FROM sign WHERE id="{id_}"')
    rows = cur.fetchall()
    return rows[0][0]

# ID 중복 체크 함수
def checkOverlap(id_):
    cur.execute(f'SELECT id FROM sign WHERE id="{id_}"')
    rows = cur.fetchall()
    if rows:
        return True
    else:
        return False 
    
# 앱으로부터 로그인 데이터를 받는 함수
@app.route('/login_confirm', methods=['GET', 'POST'])
def login_confirm():
    id = request.args.get('id', 'id')
    pwd = request.args.get('pwd', 'pwd')
    if pwd == getPw(id): # 데이터베이스에 저장된 ID에 대한 비밀번호 값이 입력한 값과 동일할 경우, ture 반환
        session['id'] = id # 세션 이용하여 로그인 구현
        temp = {"id" : id, "success" : "true"}
        return jsonify(temp)
    else:
        temp = {"id" : id, "success" : "false"}
        return jsonify(temp)

# 로그아웃 함수, 필요없을 수도
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

'''
# 데이터베이스 저장된 모든 값 출력
@app.route('/admin')
def admin():
    cur.execute("SELECT * FROM sign")
    rows = cur.fetchall()
    return jsonify(rows)

# 데이터베이스 초기화
@app.route('/remove')
def remove():
    cur.execute("DELETE FROM sign")
    return "done"
'''

# ID에 대한 데이터 값 반환
@app.route('/data')
def data():
    id = request.args.get('id', 'id')
    cur.execute(f'SELECT SN FROM sign WHERE id="{id}"')
    rows = cur.fetchall()
    if rows:
        temp = {"SN" : rows[0][0]}
        return jsonify(temp)
    else:
        return "error"

# 센서로부터 IP 값을 받아오는 함수
@app.route('/ip')
def ip():
    insideIp = request.args.get('inside', '127.0.0.1')
    outsideIp = request.args.get('outside', '192.168.0.1')
    SN = request.args.get('SN', 'SN')

    temp = {"inside": insideIp, "outside": outsideIp, "SN": SN}
    return jsonify(temp)

# 처음 실행시 DB가 없을 경우 생성
try:
    conn.execute('CREATE TABLE sign(ID TEXT, PW TEXT, SN TEXT)')
except Exception as e:
    print("already", e)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=4999)

