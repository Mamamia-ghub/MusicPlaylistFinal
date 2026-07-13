import os
from flask import Flask, render_template
from models import db
from utils import register_utils 

def create_app():
    """Implements the mandatory Application Factory Pattern requirement."""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-dev-token-999')
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'music_vault.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from routes.main import main_bp
    from routes.auth import auth_bp
    from routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    register_utils(app)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('base.html', error_title="404 Not Found", error_message="The requested track matrix route was not located on this platform server."), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('base.html', error_title="500 Internal Error", error_message="An internal dependency exception crash interrupted processing."), 500

    with app.app_context():
        db.create_all()

    return app



