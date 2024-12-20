from fasthtml.common import * 

from passlib.context import CryptContext

from functools import wraps

custom_styles = Style("""
.mw-960 { max-width: 960px; }
.mw-480 { max-width: 480px; }
.mx-auto { margin-left: auto; margin-right: auto; }

""")

app, rt = fast_app(live=True, debug=True, hdrs=(custom_styles,))

# all future code goes in here

serve()
