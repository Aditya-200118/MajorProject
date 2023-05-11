import dash
from flask import Flask
from flask.helpers import get_root_path
from flask_login import login_required
from app.helpers import usd
from config import BaseConfig
from flask_session import Session


external_stylesheets = [
    {
        'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU',
        'crossorigin': 'anonymous'
    },
]   

external_scripts = [
    {
        'src': 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/js/bootstrap.bundle.min.js',
        'integrity': 'sha384-/bQdsTh/da6pkI1MST/rWKFNjaCP5gBSY4sEBT38Q/9RBh9AH40zEOg7Hlq2THRZ',
        'crossorigin': 'anonymous'
    }
]


def create_app():
    server = Flask(__name__)

    server.config.from_object(BaseConfig)
    server.config["TEMPLATES_AUTO_RELOAD"] = True

    server.jinja_env.filters['usd'] = usd

    from app.dashapp1.layout import layout as layout1
    from app.dashapp1.callbacks import register_callbacks as register_callbacks1
    register_dashapps(server, 'Growth Chart', 'dashapp1', layout1, register_callbacks1)

    from app.dashapp3.layout import layout as layout3
    from app.dashapp3.callbacks import register_callbacks as register_callbacks3
    register_dashapps(server, 'World Indices', 'dashapp3', layout3, register_callbacks3)
    
    from app.dashapp7.layout import layout as layout7
    from app.dashapp7.callback import register_callbacks as register_callbacks7
    register_dashapps(server, 'Option Chain (U.S.A)', 'dashapp7', layout7, register_callbacks7)

    from app.dashapp8.layout import layout as layout8
    from app.dashapp8.callbacks import register_callbacks as register_callbacks8
    register_dashapps(server, "Option Chain (India)", 'dashapp8', layout8, register_callbacks8)

    from app.dashapp9.layout2 import layout as layout9
    from app.dashapp9.callbacks import register_callbacks as register_callbacks9
    register_dashapps(server, "Analysis", 'dashapp9', layout9, register_callbacks9)
    
    register_extensions(server)

    register_blueprints(server)

    Session(server)

    return server