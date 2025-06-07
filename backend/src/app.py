from flask import Flask, jsonify
from routes_embedding import embedding_bp

app = Flask(__name__)
app.register_blueprint(embedding_bp)


@app.route("/health", methods=["GET"])
def health() -> tuple:
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
