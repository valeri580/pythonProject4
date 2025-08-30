from pathlib import Path
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import CSRFProtect
from models import db, User
from forms import RegisterForm, LoginForm, ProfileForm, PasswordChangeForm, EmptyForm
from config import DevelopmentConfig

BASE_DIR = Path(__file__).resolve().parent
instance_dir = BASE_DIR / "instance"
instance_dir.mkdir(exist_ok=True)

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, instance_path=str(instance_dir))
    app.config.from_object(DevelopmentConfig)

    # Инициализация расширений
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    login_manager = LoginManager(app)
    login_manager.login_view = "login"
    login_manager.login_message = "Пожалуйста, войдите для доступа к этой странице."

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Делаем форму выхода доступной во всех шаблонах
    @app.context_processor
    def inject_forms():
        return {"logout_form": EmptyForm()}

    # Маршруты
    @app.get("/")
    def index():
        return render_template("index.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("profile"))
        form = RegisterForm()
        if form.validate_on_submit():
            user = User(name=form.name.data.strip(), email=form.email.data.lower().strip())
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Регистрация успешна. Теперь войдите.", "success")
            return redirect(url_for("login"))
        return render_template("register.html", form=form)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("profile"))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data.lower().strip()).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash("Добро пожаловать!", "success")
                next_page = request.args.get("next")
                return redirect(next_page or url_for("profile"))
            flash("Неверная почта или пароль.", "danger")
        return render_template("login.html", form=form)

    @app.post("/logout")
    @login_required
    def logout():
        form = EmptyForm()
        if form.validate_on_submit():
            logout_user()
            flash("Вы вышли из аккаунта.", "info")
        return redirect(url_for("index"))

    @app.get("/profile")
    @login_required
    def profile():
        return render_template("profile.html")

    @app.route("/profile/edit", methods=["GET", "POST"])
    @login_required
    def edit_profile():
        profile_form = ProfileForm(original_email=current_user.email)
        pass_form = PasswordChangeForm()

        # Обработка сохранения имени/почты
        if profile_form.submit_info.data and profile_form.validate_on_submit():
            if not current_user.check_password(profile_form.current_password_for_info.data):
                flash("Неверный текущий пароль для подтверждения изменений.", "danger")
            else:
                current_user.name = profile_form.name.data.strip()
                current_user.email = profile_form.email.data.lower().strip()
                db.session.commit()
                flash("Профиль обновлён.", "success")
                return redirect(url_for("profile"))

        # Обработка смены пароля
        elif pass_form.submit_pass.data and pass_form.validate_on_submit():
            if not current_user.check_password(pass_form.current_password.data):
                flash("Неверный текущий пароль.", "danger")
            else:
                current_user.set_password(pass_form.new_password.data)
                db.session.commit()
                flash("Пароль успешно обновлён.", "success")
                return redirect(url_for("profile"))

        # При GET подставим текущие значения в форму профиля
        if request.method == "GET":
            profile_form.name.data = current_user.name
            profile_form.email.data = current_user.email

        return render_template("edit_profile.html", profile_form=profile_form, pass_form=pass_form)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)