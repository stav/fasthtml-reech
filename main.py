# ruff: noqa: F405, F403, F811

from fasthtml.common import *

from db import users
from components import Dashboard, LogForm, Logout, Reach, styles
from password import basic_auth, get_password_hash, verify_password

app, rt = fast_app(live=True, debug=True, hdrs=[styles])

User = users.dataclass()


@rt("/register")
def get():
    return Container(
        Article(
            H1("Register"),
            LogForm("Register", "/register"),
            Hr(),
            P("Already have an account? ", A("Login", href="/login")),
            cls="mw-480 mx-auto",
        )
    )


@rt("/register")
def post(email: str, password: str):
    try:
        users[email]
        return "User already exists"
    except NotFoundError:
        new_user = User(email=email, password=get_password_hash(password))

        users.insert(new_user)

        return HttpHeader("HX-Redirect", "/login")


@rt("/login")
def get():
    return Container(
        Article(
            H1("Login"),
            LogForm("Login", target="/login"),
            Hr(),
            P("Want to create an Account? ", A("Register", href="/register")),
            cls="mw-480 mx-auto",
        )
    )


@rt("/login")
def post(session, email: str, password: str):
    try:
        user = users[email]
    except NotFoundError:
        return "Email or password are incorrect"

    if not verify_password(password, user.password):
        return "Email or password are incorrect"

    session["auth"] = user.email

    return HttpHeader("HX-Redirect", "/dashboard")


@rt("/dashboard")
@basic_auth
def get(session):
    return Dashboard()


@rt("/reach")
@basic_auth
def post(session, url: str):
    return Reach(url)


@rt("/logout")
def post(session):
    return Logout(session)


serve()
