## Copyright Kakusui LLC 2024 (https://kakusui.org) (https://github.com/Kakusui)
## Use of this source code is governed by a GNU General Public License v3.0
## license that can be found in the LICENSE file.

## built-in libraries
from logging.handlers import RotatingFileHandler

import os
import logging

## third-party libraries
from flask import Flask, render_template, jsonify, request, abort
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv

##-------------------start-of-setup_app()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def setup_app(app:Flask) -> bool:

    ## Load Environment Variables
    load_dotenv()

    try:
        ## get the path to this file
        path_to_flag = os.path.join(os.path.dirname(__file__), 'local_flag')
        assert os.path.exists(path_to_flag)

        os.environ['FLASK_ENV'] = 'development'

        is_local = True
        
    except AssertionError:
        is_local = False

    if(os.getenv('FLASK_ENV') == 'development'):
        app.config['SERVER_NAME'] = 'localhost:5000'
    else:
        app.config['SERVER_NAME'] = 'kakusui.org'

    ## Store root API key
    app.config['ROOT_API_KEY'] = os.getenv('ROOT_API_KEY')

    ## Setup logging
    if(not os.path.exists('logs')):
        os.mkdir('logs')

    file_handler = RotatingFileHandler('logs/myapp.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))

    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.DEBUG)
    app.logger.info('Application Startup')

    return is_local

##-------------------start-of-require_api_key()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## for now, as we don't want just anyone to access the API, we require root API key
def require_api_key(func):

    def decorated_function(*args, **kwargs):

        api_key = request.headers.get('Authorization')
        if(not api_key or api_key != f"Bearer {os.getenv('ROOT_API_KEY')}"):
            abort(401)  ## Unauthorized

        return func(*args, **kwargs)
    
    return decorated_function

##-----------------------------------------start-of-main----------------------------------------------------------------------------------------------------------------------------------------------------------

app = Flask(__name__)

CORS(app, resources={r"/v1/*": {"origins": ["https://kakusui.org", "http://localhost:5000"]}})

is_local = setup_app(app)

## Routes

## Home Page
@app.route('/')
def home():
    app.logger.debug("Serving Home Page")
    return render_template('home.html')

## Okisouchi Pages
@app.route('/okisouchi/')
def okisouchi():
    app.logger.debug("Serving Okisouchi Page")
    return render_template('okisouchi/okisouchi.html')

@app.route('/okisouchi/tos/')
def tos():
    app.logger.debug("Serving TOS Page")
    return render_template('okisouchi/tos/tos.html')

@app.route('/okisouchi/privacypolicy/')
def privacy_policy():
    app.logger.debug("Serving Privacy Policy Page")
    return render_template('okisouchi/privacypolicy/privacypolicy.html')


## Kairyou Pages
@app.route('/kairyou/')
def kairyou():
    app.logger.debug("Serving Kairyou Page")
    return render_template('kairyou/kairyou.html', api_key=os.getenv('ROOT_API_KEY'), is_local=is_local)

## Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    app.logger.error(f"404 Error: {e}, Page Not Found")
    return render_template('/error_pages/404.shtml'), 404

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error(f"500 Error: {e}, Internal Server Error")
    return render_template('/error_pages/500.shtml'), 500

@app.errorhandler(403)
def forbidden(e):
    app.logger.error(f"403 Error: {e}, Forbidden")
    return render_template('/error_pages/403.shtml'), 403

## API Endpoints

@app.route('/', subdomain='api')
def api_home():
    return jsonify({"message": "Welcome to the API"})

@app.route('/v1/kairyou', subdomain='api', methods=["GET", "POST", "OPTIONS"])
@cross_origin(origins=["https://kakusui.org", "http://localhost:5000"])
@require_api_key
def kairyou():
    return jsonify({"message": "Wow you have access to the API"})

if(__name__ == '__main__'):
    app.run(debug=True)