from flask import Flask, request, redirect, url_for, render_template, session, jsonify
import sqlite3
conn = sqlite3.connect("Test.db", check_same_thread=False)
cur = conn.cursor()

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

# 데이터베이스에 회원가입 데이터를 넣는 메소드
def signup_db(id, pw, sn):
    cur.execute('INSERT INTO sign VALUES (?, ?, ?)', (id, pw, sn))
    conn.commit()
    print("good", id, pw, sn)