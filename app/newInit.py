from flask import Flask


app = Flask(__name__)

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)


from app import routes, models
