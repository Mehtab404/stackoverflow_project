from flask import Flask, jsonify, send_from_directory
import pandas as pd
import os
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app, resources={r"/api/*": {"origins": "*"}})

def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "project_overflow/top_10_tags_trend.csv")
    if not os.path.exists(file_path):
        return {}  # Return an empty dictionary if the file is missing
    df = pd.read_csv(file_path, index_col=0)
    return df.to_dict(orient="index")

@app.route("/api/data", methods=["GET"])
def get_data():
    data = load_data()
    return jsonify(data)

@app.route('/style.css')
def serve_css():
    return send_from_directory(app.static_folder, "style.css")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
