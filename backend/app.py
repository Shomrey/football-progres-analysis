from flask import Flask
from flask_cors import CORS

from analysis.analysis_api import app_analysis


app = Flask(__name__)
CORS(app)

app.register_blueprint(app_analysis)

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)