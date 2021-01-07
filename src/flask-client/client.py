import os
import requests
import json

from flask import Flask, request, redirect, render_template

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.dirname(__file__)

ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg"]


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]

        filename = file.filename
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        # check filename isn't empty
        if filename == "":
            return redirect(request.url)

        # check file is allowed
        if file and allowed_file(filename):
            file.save(file_path)
            url = "http://localhost:5000/uploader"
            send_image = open(file_path, "rb")
            files = {"file": send_image}

            r = requests.post(url, files=files)
            send_image.close()
            os.remove(file_path)

            pred = json.loads(r.content.decode("utf-8"))
            return render_template("upload.html") + render_template(
                "image_class.html", pred=pred
            )

    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5001)
