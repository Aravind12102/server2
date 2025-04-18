from flask import Flask, request, jsonify
from Gemini import analyze_form_with_gemini

app = Flask(__name__)

form_result_cache = {
    "response": None
}

@app.route("/home", methods=["POST"])
def home():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' in JSON payload"}), 400

    url = data["url"]
    result = analyze_form_with_gemini(url)
    form_result_cache["response"] = result

    return jsonify({"message": "Form analyzed successfully"}), 200

@app.route("/show", methods=["GET"])
def show():
    if form_result_cache["response"] is None:
        return jsonify({"error": "No analysis available. Please POST to /home first."}), 400

    return jsonify({"response": form_result_cache["response"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8501, debug=True)
