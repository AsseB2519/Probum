from flask import Flask

main = Flask(__name__)

from routes import *

main.run(debug=True,port=5001)