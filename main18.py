from flask import Flask, render_template, request, make_response
from imdbmodels import Imdbuser, Filmadatb, db
import uuid

app = Flask(__name__)
db.create_all()


@app.route("/")
def index():
    session_token = request.cookies.get("session_token")
    if session_token:
        user = db.query(Imdbuser).filter_by(session_token=session_token).first()
        return render_template("table.html", name=user, filmek=db.query(Filmadatb))
    else:
        return render_template("table.html")


@app.route("/form", methods=["POST"])
def contact():
    username = request.form.get("username")
    password = request.form.get("password")

    db_user = db.query(Imdbuser).filter(Imdbuser.name == username).first()

    if db_user:
        if db_user.password == password:
            session_token = str(uuid.uuid4())

            db_user.session_token = session_token
            db.add(db_user)
            db.commit()

            response = make_response(render_template("table.html", filmek=db.query(Filmadatb), name=username))
            response.set_cookie("session_token", session_token, httponly=True, samesite='Strict')
    else:
        response = render_template("table.html")
    return response

@app.route("/reg", methods=["POST"])
def reg():
    username = request.form.get("regusername")
    password = request.form.get("regpassword")

    user = Imdbuser(name=username, password=password)
    session_token = str(uuid.uuid4())
    user.session_token = session_token

    db.add(user)
    db.commit()

    response = make_response(render_template("table.html", filmek=db.query(Filmadatb), name = username))
    response.set_cookie("session_token", session_token, httponly=True, samesite='Strict')
    return response

@app.route("/logoff", methods=["POST"])
def kilepes():
    response = make_response(render_template("table.html"))
    response.set_cookie("session_token", expires = 0)
    return response

if __name__ == '__main__':
    app.run()


