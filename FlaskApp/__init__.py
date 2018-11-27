from flask import Flask, render_template
from content_management import Content

TOPIC_DICT = Content()

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def homepage():
    return render_template("main.html")

@app.route('/python/')
def python():
    return render_template("python.html", TOPICS=TOPIC_DICT["Python"])

@app.route('/luottokortti/')
def luottokortti():
    return render_template("luottokortti.html")


if __name__ == "__main__":
    app.run()
      
