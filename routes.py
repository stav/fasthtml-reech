# ruff: noqa: F405, F403, F811

from fasthtml.common import *

from auth import basic_auth, get_login, get_register, post_login, post_register
from components import Dashboard, Logout, Reach


def route(rt):

    @rt("/register")
    def get():
        return get_register()

    @rt("/register")
    def post(email: str, password: str):
        return post_register(email, password)

    @rt("/login")
    def get():
        return get_login()

    @rt("/login")
    def post(session, email: str, password: str):
        return post_login(session, email, password)

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
