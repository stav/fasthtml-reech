# ruff: noqa: F405, F403

from bs4 import BeautifulSoup
from fasthtml.common import *
import requests


styles = Style(
    """
.mw-960 { max-width: 960px; }
.mw-480 { max-width: 480px; }
.mx-auto { margin-left: auto; margin-right: auto; }

"""
)


def LogForm(btn_text, target):
    return Form(
        Input(id="email", type="email", placeholder="Email", required=True),
        Input(id="password", type="password", placeholder="Password", required=True),
        Button(btn_text, type="submit"),
        Span(id="error", style="color:red"),
        hx_post=target,
        hx_target="#error",
    )


def Dashboard():
    return Container(
        H1("Dashboard"),
        Form(
            Group(
                Input(id="url", type="url", placeholder="Enter URL", required=True),
                Button("Reach", type="submit"),
            ),
            hx_post="/reach",
        ),
        Button("Logout", hx_post="/logout"),
    )


def Reach(url: str):
    print("Data received in /reach POST request:", type(url), url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    print("Contents of the page:", soup.text)
    return Card(Code(soup.text), header=A(url, href=url))


def Logout(session):
    # session.clear()
    del session["auth"]
    return HttpHeader("HX-Redirect", "/login")
