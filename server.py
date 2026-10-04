from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Test route
@app.route("/")
def home():
    return "Rent and Reuse backend is running"


# Upload image
@app.route("/upload-image", methods=["POST"])
def upload_image():

    if "image" not in request.files:
        return jsonify({"error": "No image selected"}), 400

    image = request.files["image"]

    if image.filename == "":
        return jsonify({"error": "No image selected"}), 400

    filename = image.filename

    image.save(
        os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )
    )

    return jsonify({
        "message": "Image uploaded successfully",
        "imageURL": "/uploads/" + filename
    })


# Show uploaded images
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


# Start server
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)