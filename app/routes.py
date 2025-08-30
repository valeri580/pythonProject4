from flask import Blueprint, render_template, request

bp = Blueprint("main2", __name__)

from flask import Blueprint, render_template, request

bp = Blueprint("main2", __name__)  # имя блюпринта может быть main2

@bp.route("/", methods=["GET", "POST"])
def blog():
    data = {"name": "", "city": "", "hobbies": "", "age": ""}
    if request.method == "POST":
        data["name"] = request.form.get("name", "").strip()
        data["city"] = request.form.get("city", "").strip()
        data["hobbies"] = request.form.get("hobbies", "").strip()
        data["age"] = request.form.get("age", "").strip()
    return render_template("blog.html", data=data)
