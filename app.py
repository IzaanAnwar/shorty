from flask import Flask, render_template, request
import string
import random

app = Flask(__name__)
REDIS_HOST='localhost'
REDIS_PORT=6379



def shortenUrl(urlRec: str) -> str:
    allowed_chars = string.ascii_letters + string.digits
    return "".join(random.choice(allowed_chars) for _ in range(5))


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        urlRec = request.form.get("originalUrl")
        shortUrl = shortenUrl(urlRec=urlRec)
        return render_template("index.html", shortened_url=shortUrl)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
