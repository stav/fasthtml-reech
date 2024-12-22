# ruff: noqa: F405, F403

import csv
import requests

from io import StringIO
from fasthtml.common import *


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
    response = requests.get(url)
    rows = []

    csv_reader = csv.reader(StringIO(response.text))
    for row in csv_reader:
        month, year, _, current, _, expected, *_ = row
        try:
            assert year.isdigit()
            float(current)
            float(expected)
            data = (
                month,
                year,
                f"{float(current):,.1f}",
                f"{float(expected):,.1f}",
            )
            rows.append(data)
            print(data)

        except (AssertionError, ValueError):
            print("Invalid data:", row)

    return Card(Pre(rows), header=A(url, href=url))


def Logout(session):
    # session.clear()
    del session["auth"]
    return HttpHeader("HX-Redirect", "/login")
