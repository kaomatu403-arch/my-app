from flask import Flask, render_template

app = Flask(__name__)

@app.route('/show_signin')
def show_signin():
    # templatesフォルダの中にある sign_in.html を表示する
    return render_template('sign_in.html')

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)