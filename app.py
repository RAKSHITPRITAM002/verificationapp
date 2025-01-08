from flask import Flask, request, jsonify, render_template, session
import random
import string
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)
app.secret_key = 'secret_key'
os.makedirs('static/captcha', exist_ok=True)

def generate_captcha_text():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=1))

def create_captcha_image(text, filename):
    img = Image.new('RGB', (50, 50), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((10, 10), text, fill=(0, 0, 0), font=font)
    img.save(filename)

@app.route('/')
def index():
    session['captcha_values'] = []
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_captcha():
    if len(session['captcha_values']) >= 6:
        return jsonify({'error': 'All fields are filled!'}), 400
    
    text = generate_captcha_text()
    session['captcha_values'].append(text)
    filename = f'static/captcha/{len(session["captcha_values"])}.png'
    create_captcha_image(text, filename)
    return jsonify({'image_url': f'/{filename}'})

@app.route('/validate', methods=['POST'])
def validate_captcha():
    user_input = request.json.get('inputs', [])
    if user_input == session.get('captcha_values', []):
        return jsonify({'status': 'success', 'message': 'Verification successful!'})
    else:
        session['captcha_values'] = []
        return jsonify({'status': 'failure', 'message': 'Verification failed. Try again.'})

if __name__ == '__main__':
    app.run(debug=True)
