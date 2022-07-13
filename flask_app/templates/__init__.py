from flask import Flask
app = Flask('app', static_folder='flask_app/static', template_folder='flask_app/templates')
app.secret_key = "shhhhhh"