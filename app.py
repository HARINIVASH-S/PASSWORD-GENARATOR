from flask import Flask, render_template, request
import random
import string

app = Flask(__name__, static_url_path='/static')

def generate_password(length):
    basic_chars = string.ascii_letters + string.digits + string.punctuation
    
    all_chars = basic_chars 
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
        score += 1

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
    if request.method == 'POST':
        try:
            length = int(request.form['length'])
            password = generate_password(length)
            strength, progress = check_strength(password)
        except:
            password = 'Error generating password!'
    return render_template('index.html', password=password, strength=strength, progress=progress)

@app.route('/check', methods=['GET', 'POST'])
def check():
    user_password = ''
    strength = ''
    progress = 0
    if request.method == 'POST':
        user_password = request.form['user_password']
        strength, progress = check_strength(user_password)
    return render_template('strength_check.html', password=user_password, strength=strength, progress=progress)

if __name__ == '__main__':
    app.run(debug=True)
