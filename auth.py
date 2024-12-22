# ruff: noqa: F405, F403, F811

from functools import wraps
from passlib.context import CryptContext

from fasthtml.common import *

from db import users
from components import LogForm

User = users.dataclass()


def get_register():
    return Container(
        Article(
            H1("Register"),
            LogForm("Register", "/register"),
            Hr(),
            P("Already have an account? ", A("Login", href="/login")),
            cls="mw-480 mx-auto",
        )
    )


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def post_register(email: str, password: str):
    try:
        users[email]
        return "User already exists"
    except NotFoundError:
        new_user = User(email=email, password=get_password_hash(password))

        users.insert(new_user)

        return HttpHeader("HX-Redirect", "/login")


def get_login():
    return Container(
        Article(
            H1("Login"),
            LogForm("Login", target="/login"),
            Hr(),
            P("Want to create an Account? ", A("Register", href="/register")),
            cls="mw-480 mx-auto",
        )
    )


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def post_login(session, email: str, password: str):
    try:
        user = users[email]
    except NotFoundError:
        return "Email or password are incorrect"

    if not verify_password(password, user.password):
        return "Email or password are incorrect"

    session["auth"] = user.email

    return HttpHeader("HX-Redirect", "/dashboard")


def basic_auth(f):
    @wraps(f)
    def wrapper(session, *args, **kwargs):
        if "auth" not in session:
            return Response("Not Authorized", status_code=401)
        return f(session, *args, **kwargs)

    return wrapper
