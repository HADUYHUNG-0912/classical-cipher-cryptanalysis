"""
demo/app.py — Web demo for Classical Cipher Cryptanalysis Toolkit
Run from project root: python demo/app.py
Then open: http://127.0.0.1:5000
"""
import time
import sys
import csv
from pathlib import Path
from flask import Flask, request, jsonify, render_template

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from caesar.cipher import encrypt as caesar_encrypt, decrypt as caesar_decrypt
from caesar.attack import break_caesar
from vigenere.cipher import encrypt as vigenere_encrypt, decrypt as vigenere_decrypt
from vigenere.attack import break_vigenere, estimate_key_length
from playfair.cipher import encrypt as playfair_encrypt, decrypt as playfair_decrypt
from playfair.attack import break_playfair

app = Flask(__name__, template_folder='templates', static_folder='static')


def _timed(fn, *args, **kwargs):
    t0 = time.perf_counter()
    result = fn(*args, **kwargs)
    return result, round((time.perf_counter() - t0) * 1000, 2)


def _load_csv(filename):
    path = PROJECT_ROOT / 'experiments' / 'results' / filename
    if not path.exists():
        return []
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f))


# ─────────────────────── PAGES ───────────────────────
@app.route('/')
def index():
    return render_template('index.html')


# ─────────────────────── CAESAR ───────────────────────
@app.route('/api/caesar/encrypt', methods=['POST'])
def caesar_enc():
    d = request.get_json()
    text, key = d.get('text', '').strip(), int(d.get('key', 3))
    if not text:
        return jsonify({'error': 'Vui lòng nhập văn bản'}), 400
    result, ms = _timed(caesar_encrypt, text, key)
    return jsonify({'result': result, 'key': key, 'time_ms': ms})


@app.route('/api/caesar/decrypt', methods=['POST'])
def caesar_dec():
    d = request.get_json()
    text, key = d.get('text', '').strip(), int(d.get('key', 3))
    if not text:
        return jsonify({'error': 'Vui lòng nhập văn bản'}), 400
    result, ms = _timed(caesar_decrypt, text, key)
    return jsonify({'result': result, 'key': key, 'time_ms': ms})


@app.route('/api/caesar/attack', methods=['POST'])
def caesar_atk():
    d = request.get_json()
    ct = d.get('text', '').strip()
    if not ct:
        return jsonify({'error': 'Vui lòng nhập văn bản mật mã'}), 400
    (plain, key), ms = _timed(break_caesar, ct)
    return jsonify({'result': plain, 'key': key, 'time_ms': ms})


# ─────────────────────── VIGENÈRE ───────────────────────
@app.route('/api/vigenere/encrypt', methods=['POST'])
def vigenere_enc():
    d = request.get_json()
    text, key = d.get('text', '').strip(), d.get('key', '').strip().upper()
    if not text or not key:
        return jsonify({'error': 'Vui lòng nhập văn bản và khóa'}), 400
    result, ms = _timed(vigenere_encrypt, text, key)
    return jsonify({'result': result, 'key': key, 'time_ms': ms})


@app.route('/api/vigenere/decrypt', methods=['POST'])
def vigenere_dec():
    d = request.get_json()
    text, key = d.get('text', '').strip(), d.get('key', '').strip().upper()
    if not text or not key:
        return jsonify({'error': 'Vui lòng nhập văn bản và khóa'}), 400
    result, ms = _timed(vigenere_decrypt, text, key)
    return jsonify({'result': result, 'key': key, 'time_ms': ms})


@app.route('/api/vigenere/attack', methods=['POST'])
def vigenere_atk():
    d = request.get_json()
    ct = d.get('text', '').strip()
    if not ct:
        return jsonify({'error': 'Vui lòng nhập văn bản mật mã'}), 400
    (plain, key), ms = _timed(break_vigenere, ct)
    est = estimate_key_length(ct)
    return jsonify({'result': plain, 'key': key, 'estimated_key_len': est, 'time_ms': ms})


# ─────────────────────── PLAYFAIR ───────────────────────
@app.route('/api/playfair/encrypt', methods=['POST'])
def playfair_enc():
    d = request.get_json()
    text, key = d.get('text', '').strip(), d.get('key', '').strip()
    if not text or not key:
        return jsonify({'error': 'Vui lòng nhập văn bản và khóa'}), 400
    result, ms = _timed(playfair_encrypt, text, key)
    return jsonify({'result': result, 'key': key.upper(), 'time_ms': ms})


@app.route('/api/playfair/decrypt', methods=['POST'])
def playfair_dec():
    d = request.get_json()
    text, key = d.get('text', '').strip(), d.get('key', '').strip()
    if not text or not key:
        return jsonify({'error': 'Vui lòng nhập văn bản và khóa'}), 400
    result, ms = _timed(playfair_decrypt, text, key)
    return jsonify({'result': result, 'key': key.upper(), 'time_ms': ms})


@app.route('/api/playfair/attack', methods=['POST'])
def playfair_atk():
    d = request.get_json()
    ct = d.get('text', '').strip()
    iters = int(d.get('iterations', 2000))
    restarts = int(d.get('restarts', 5))
    if not ct:
        return jsonify({'error': 'Vui lòng nhập văn bản mật mã'}), 400
    (plain, key), ms = _timed(break_playfair, ct, iterations=iters, restarts=restarts)
    return jsonify({'result': plain, 'key': key, 'time_ms': ms})


# ─────────────────────── DATA API ───────────────────────
@app.route('/api/results/caesar')
def results_caesar():
    return jsonify(_load_csv('caesar_results.csv'))


@app.route('/api/results/vigenere')
def results_vigenere():
    return jsonify(_load_csv('vigenere_results.csv'))


@app.route('/api/results/playfair')
def results_playfair():
    return jsonify(_load_csv('playfair_results.csv'))


# ─────────────────────── ENTRY POINT ───────────────────────
if __name__ == '__main__':
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    print()
    print('=' * 60)
    print('  Cryptanalysis Demo - Classical Cipher Toolkit')
    print('  Open browser: http://127.0.0.1:5000')
    print('=' * 60)
    print()
    app.run(debug=False, port=5000, host='127.0.0.1')
