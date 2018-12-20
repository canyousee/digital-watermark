from flask import Blueprint

home = Blueprint('home', 'public.views', url_prefix='/')

auth = Blueprint('auth', 'auth.views', url_prefix='/auth')

all_blueprints = (home, auth,)