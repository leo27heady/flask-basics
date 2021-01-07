from flask import Flask, request, jsonify
import cv2

# from tensorflow import keras

import os


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.dirname(__file__)

model = None


def read_image(file_path):
    image = cv2.imread(file_path)
    image = cv2.resize(image, (512, 512))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    os.remove(file_path)
    return image


# def load_model(model_path):
#     return models.load_model(model_path)


@app.route("/")
def index():
    return "Hello world!"


@app.route("/uploader", methods=["POST"])
def get_file():
    f = request.files["file"]
    f.save(os.path.join(app.config["UPLOAD_FOLDER"], f.filename))

    img = read_image(os.path.join(app.config["UPLOAD_FOLDER"], f.filename))
    print(img.shape)
    # predict = model.predict(img)
    print("request url:", request.url)
    response = {"class_id": 3}

    return jsonify(response)


if __name__ == "__main__":

    model_path = app.config["UPLOAD_FOLDER"] + "\\model\\weights.h5"

    # model = load_model(filename)
    app.run(debug=True, host="localhost", port=5000)
