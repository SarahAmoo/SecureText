from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def caesar_cipher(text: str, shift: int, decrypt: bool = False) -> str:
    if decrypt:
        shift = -shift
    result = []
    for char in text:
        if char.isupper():
            start = ord("A")
            result.append(chr((ord(char) - start + shift) % 26 + start))
        elif char.islower():
            start = ord("a")
            result.append(chr((ord(char) - start + shift) % 26 + start))
        else:
            result.append(char)
    return "".join(result)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/cipher", methods=["POST"])
def cipher():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    text = data.get("text", "")
    raw = data.get("shift", "")

    if not raw:
        return jsonify({"error": "Please enter a Secret Shift Key."}), 400

    try:
        shift = int(raw)
    except (ValueError, TypeError):
        return jsonify({"error": "The shift key must be a whole number (e.g., 3)."}), 400

    if not text:
        return jsonify({"error": "Please enter a message to process."}), 400

    decrypt = data.get("decrypt", False)
    try:
        output = caesar_cipher(text, shift, decrypt=decrypt)
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

    action = "Decryption" if decrypt else "Encryption"
    return jsonify({"output": output, "message": f"{action} complete. Shift used: {shift}."})


if __name__ == "__main__":
    import sys
    if "--prod" in sys.argv:
        from waitress import serve
        serve(app, host="0.0.0.0", port=5000)
    else:
        app.run(debug=True)
