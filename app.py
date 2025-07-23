from flask import Flask, render_template, request
import random
import string

app = Flask(__name__)

def generate_password(length):
    basic_chars = string.ascii_letters + string.digits + string.punctuation
    extras = ' \t\n±§©®'
    all_chars = basic_chars + extras
    return ''.join(random.choice(all_chars) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def index():
    password = ''
    if request.method == 'POST':
        try:
            length = int(request.form['length'])
            password = generate_password(length)
        except:
            password = 'Error generating password!'
    return render_template('index.html', password=password)

if __name__ == '__main__':
    app.run(debug=True)
