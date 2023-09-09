from flask import Flask, render_template, url_for


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wiki.html')
def wiki():
    return render_template('wiki.html')

@app.route('/credits.html')
def credits():
    return render_template('credits.html')

if __name__ == "__main__":
    app.run(debug = True)

