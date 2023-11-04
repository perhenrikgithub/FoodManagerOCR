import os
from flask import Flask, Response, jsonify, request
from werkzeug.utils import secure_filename
from src.core.ocr_analyse import make_gpt_request


UPLOAD_FOLDER = "src/receipts"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def _allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/media/upload", methods=["POST"])
def upload_media() -> Response:
    print(request.files)
    if "file" not in request.files:
        return jsonify({"error": "media not provided or not correct filetype"}), 400
    
    file = request. files["file"]
    if not file.filename:
        return jsonify({"error": "no file selected"}), 400
    
    if file and _allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(path)
        text = make_gpt_request(path)
        print(text)
        return jsonify({"msg": text}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
