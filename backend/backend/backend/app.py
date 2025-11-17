from flask import Flask, request, jsonify, send_file, render_template, redirect
from flask_cors import CORS
from database import create_tables
import utils
import sqlite3
import io
from openpyxl import Workbook

create_tables()

app = Flask(__name__)
CORS(app)
app.config['JSON_SORT_KEYS'] = False

@app.route('/')
def index():
    # redirect to login server page (example)
    return redirect('/templates/login.html')

@app.route('/templates/login.html')
def login_page():
    return render_template('login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/admin/add_question', methods=['GET', 'POST'])
def admin_add_question():
    if request.method == 'GET':
        return render_template('admin_add_question.html')
    data = request.form
    utils.add_question(data['question'], data['option1'], data['option2'], data['option3'], data['option4'], data['answer'])
    return 'Added', 201

@app.route('/admin/export_results')
def admin_export_results():
    conn = sqlite3.connect('cbt.db')
    cur = conn.cursor()
    cur.execute('SELECT id, username, score, total, timestamp FROM results ORDER BY timestamp DESC')
    rows = cur.fetchall()
    conn.close()

    wb = Workbook()
    ws = wb.active
    ws.title = 'Results'
    ws.append(['ID', 'Username', 'Score', 'Total', 'Timestamp'])
    for r in rows:
        ws.append(list(r))

    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)
    return send_file(stream, as_attachment=True, download_name='cbt_results.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# ----------------- API for React frontend -----------------

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = utils.verify_user(username, password)
    if user:
        return jsonify({'ok': True, 'username': user['username'], 'role': user['role']})
    return jsonify({'ok': False, 'error': 'invalid credentials'}), 401

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    success = utils.add_user(data['username'], data['password'], role='student')
    if success:
        return jsonify({'ok': True})
    return jsonify({'ok': False, 'error': 'username taken'}), 400

@app.route('/api/start_exam', methods=['POST'])
def api_start_exam():
    data = request.json
    username = data.get('username')
    duration = data.get('duration', 300)
    exam_id, order = utils.create_exam_session(username, duration)
    return jsonify({'ok': True, 'exam_id': exam_id, 'question_order': order, 'duration': duration})

@app.route('/api/exam/<exam_id>/question/<int:idx>', methods=['GET'])
def api_get_question(exam_id, idx):
    session = utils.get_exam_session(exam_id)
    if not session:
        return jsonify({'ok': False, 'error': 'invalid exam id'}), 404
    qids = session[2].split(',')
    if idx < 0 or idx >= len(qids):
        return jsonify({'ok': False, 'error': 'index out of range'}), 400
    qid = int(qids[idx])
    q = utils.get_question_by_id(qid)
    return jsonify({
        'ok': True,
        'index': idx,
        'question': {
            'id': q[0],
            'text': q[1],
            'options': [q[2], q[3], q[4], q[5]]
        },
        'total': len(qids)
    })

@app.route('/api/submit_exam', methods=['POST'])
def api_submit_exam():
    data = request.json
    exam_id = data.get('exam_id')
    username = data.get('username')
    answers = data.get('answers', {})
    session = utils.get_exam_session(exam_id)
    if not session:
        return jsonify({'ok': False, 'error': 'invalid exam id'}), 404
    qids = session[2].split(',')
    score = 0
    total = len(qids)
    for qid_str in qids:
        qid = int(qid_str)
        correct = utils.get_answer(qid)
        selected = answers.get(str(qid))
        if selected and selected == correct:
            score += 1
    utils.save_result(username, score, total)
    return jsonify({'ok': True, 'score': score, 'total': total})

@app.route('/api/results/<username>', methods=['GET'])
def api_get_results(username):
    rows = utils.get_results_for_user(username)
    resp = [{'id': r[0], 'score': r[1], 'total': r[2], 'timestamp': r[3]} for r in rows]
    return jsonify({'ok': True, 'results': resp})

if __name__ == '__main__':
    app.run(debug=True)
