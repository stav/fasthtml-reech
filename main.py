from fasthtml.common import serve, fast_app

from components import styles
from routes import route

app, rt = fast_app(live=True, debug=True, hdrs=[styles])

route(rt)

serve()
