from flask import Flask, redirect, render_template, request, url_for
import model


app = Flask(__name__)
comments = list()
app.config["DEBUG"] = True


@app.route("/", methods=["GET", "POST"])
def index():
    # comments.clear()
    if request.method == "GET":
        return render_template("main_page.html", comments=comments)

    recom = model.predict_class(request.form["contents"])
    comments.clear()
    comments.append(recom)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()