import sqlite3
from flask import Flask, current_app, g, render_template, request, redirect
import string
import random
import os


app = Flask(__name__)
app.config['DATABASE'] = os.path.join(app.root_path, 'shorty.db')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    
def shortenUrl(urlRec: str) -> str:
    allowed_chars = string.ascii_letters + string.digits
    return "".join(random.choice(allowed_chars) for _ in range(5))


@app.route("/", methods=["GET", "POST"])
def home(): 
    if request.method == "POST":
        url = request.form.get("originalUrl")
        if not url or url == "":
            return render_template("index.html", error="Please fill the form")

        code = shortenUrl(urlRec=url)
        try:
            db = get_db()
            urlExists = db.execute(
                'SELECT code FROM url_codes WHERE url = ?',
            (url,)
        ).fetchone()
            if urlExists and urlExists['code']:
                print("hit")
                return render_template("index.html", shortened_url=f"{request.host_url}/{urlExists['code']}")
            db.execute(
                'INSERT INTO url_codes (url, code) VALUES (?,?)',
                (url, code)
            )
            db.commit()
            return render_template("index.html", shortened_url=f"{request.host_url}/{code}")
        except Exception as e:
            print("ERROR LOG -> ",e, "\n")
        return render_template("not-found.html", code=500, message="Something went wrong please try again"), 500
    return render_template("index.html")


@app.route("/<string:code>", methods=["GET"])
def goToURL(code:str):
    print(code)
    try:
        db = get_db()
        url = db.execute(
            'SELECT url FROM url_codes WHERE code = ?',
            (code,)
        ).fetchone()
        if url and url['url']:
            return redirect(location=url['url'])
        return render_template("not-found.html", code=404, message="URL NOT FOUND"), 404
    except Exception as e:
        print(e)
        return render_template("not-found.html", code=500, message="Something went wrong please try again"), 500


if __name__ == "__main__":
    app.run(debug=True)
