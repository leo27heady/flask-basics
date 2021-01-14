import os

from flask import Flask, request, jsonify
import torch
import torchvision
import cv2


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.dirname(__file__)

model = None


class DataRetriever(torch.utils.data.Dataset):
    def __init__(
        self,
        paths,
        image_size,
        preprocess=None,
    ):
        self.paths = paths
        self.image_size = image_size
        self.preprocess = preprocess

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, index):
        img = cv2.imread(self.paths[index])
        img = cv2.resize(img, self.image_size)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = self.preprocess(img)

        return img


def get_preprocess():
    return torchvision.transforms.Compose(
        [
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize(
                mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
            ),
        ]
    )


def load_model_mobilenet_v2(model_path, n_classes=5):
    global model

    model = torch.hub.load(
        "pytorch/vision:v0.6.0", "mobilenet_v2", pretrained=False
    )
    model.classifier = torch.nn.Linear(
        in_features=1280,
        out_features=n_classes,
        bias=True,
    )

    checkpoint = torch.load(model_path, map_location=torch.device("cpu"))
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()


def get_data_loader(image_path):
    data_retriever = DataRetriever(
        [image_path],
        image_size=(224, 224),
        preprocess=get_preprocess(),
    )

    loader = torch.utils.data.DataLoader(
        data_retriever, batch_size=1, shuffle=False
    )

    return loader


def predict_image(loader):
    y_pred = []
    for batch in loader:
        print(model(batch.to("cpu")))
        y_pred.extend(model(batch.to("cpu")).argmax(axis=-1).numpy())

    return int(y_pred[0])


@app.route("/")
def index():
    return "Hello world!"


@app.route("/uploader", methods=["POST"])
def get_file():
    global model

    f = request.files["file"]
    f.save(os.path.join(app.config["UPLOAD_FOLDER"], f.filename))

    image_path = os.path.join(app.config["UPLOAD_FOLDER"], f.filename)

    loader = get_data_loader(image_path)

    predict = predict_image(loader)
    os.remove(image_path)

    print("request url:", request.url)
    response = {"image_name": f.filename, "class_id": predict}

    return jsonify(response)


if __name__ == "__main__":

    model_path = app.config["UPLOAD_FOLDER"] + "\\model\\model-best.torch"

    load_model_mobilenet_v2(model_path, n_classes=5)
    app.run(debug=False, host="localhost", port=5000)
