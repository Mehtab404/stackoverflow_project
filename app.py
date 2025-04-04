from flask import Flask, jsonify, send_from_directory
import pandas as pd
import os
from flask_cors import CORS

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)

def load_data():
    # Adjusted file path - verify your file structure matches this
    file_path = os.path.join(os.path.dirname(__file__), "top_10_tags_trend.csv")
    if not os.path.exists(file_path):
        return {}
    df = pd.read_csv(file_path, index_col=0)
    return df.to_dict(orient="index")

@app.route("/api/data", methods=["GET"])
def get_data():
    data = load_data()
    return jsonify(data)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
