from fasthtml.common import serve, fast_app
from fh_altair import altair_headers

from components import styles
from routes import route

app, rt = fast_app(live=True, debug=True, hdrs=[styles, altair_headers])

route(rt)

serve()
