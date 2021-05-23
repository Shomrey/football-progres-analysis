from flask import Flask

from typing import Optional
from analysis.analysis_api import app_analysis


app = Flask(__name__)

app.register_blueprint(app_analysis)

if __name__ == "__main__":
    app.run()