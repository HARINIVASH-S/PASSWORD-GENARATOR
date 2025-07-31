from flask import Flask, render_template, request
import random
import string

app = Flask(__name__, static_url_path='/static')

def generate_password(length):
    all_chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(all_chars) for _ in range(length))

def check_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c.islower() for c in password) and any(c.isupper() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1
    if any(c.isspace() for c in password):
        score -= 1

    if score <= 1:
        return 'Weak', 20
    elif score == 2:
        return 'Moderate', 40
    elif score == 3:
        return 'Strong', 60
    elif score == 4:
        return 'Very Strong', 80
    else:
        return 'Excellent', 100

@app.route('/', methods=['GET', 'POST'])
def index():
    password = ''
    strength = ''
    progress = 0
    reveal = False

    if request.method == 'POST':
        try:
            length = int(request.form.get('length', 12))
            reveal = request.form.get('reveal') == 'yes'

            # Preserve password on copy/reveal toggle
            if request.form.get('copy') == 'true':
                password = request.form.get('password', '')
            elif request.form.get('password'):
                password = request.form.get('password')
            else:
                password = generate_password(length)

            strength, progress = check_strength(password)
        except:
            password = 'Error generating password!'
            strength = 'Error'
            progress = 0

    return render_template('index.html', password=password, strength=strength, progress=progress, reveal=reveal)

@app.route('/check', methods=['GET', 'POST'])
def check():
    user_password = ''
    strength = ''
    progress = 0

    if request.method == 'POST':
        user_password = request.form.get('user_password', '')
        if user_password:
            strength, progress = check_strength(user_password)
        else:
            strength = 'Enter a password to check.'
            progress = 0

    return render_template('strength_check.html', password=user_password, strength=strength, progress=progress)

if __name__ == '__main__':
    app.run(debug=True)
