from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "this is a secret don't tell"
# Bcrypt = Bcrypt(app)
