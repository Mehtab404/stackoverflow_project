from flask import Flask, jsonify
import pandas as pd
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def load_data():
    file_path = "project_overflow/top_10_tags_trend.csv"
    df = pd.read_csv(file_path, index_col=0)
    return df.to_dict(orient="index")

@app.route("/api/data", methods=["GET"])
def get_data():
    data = load_data()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)