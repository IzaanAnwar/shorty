from flask import Flask, render_template, request
import string
import random
import redis

app = Flask(__name__)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)




def shortenUrl(urlRec: str) -> str:
    allowed_chars = string.ascii_letters + string.digits
    return "".join(random.choice(allowed_chars) for _ in range(5))


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        urlRec = request.form.get("originalUrl")
        shortUrl = shortenUrl(urlRec=urlRec)
        shortKey = redis_client.get(urlRec)
        print(shortKey)
        if shortKey:
            return render_template("index.html", shortened_url=shortKey)

        val = redis_client.set(urlRec, shortUrl)
        if val:
            return render_template("index.html", shortened_url=shortUrl)
        return "Something went wrong!!"

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
