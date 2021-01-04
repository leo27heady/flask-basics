from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello world!"


@app.route("/uploader", methods=["POST"])
def upload_file():
    f = request.files["file"]
    print(type(f))
    print(len(f))
    print()
    f.save(f.filename)
    return "file uploaded successfully"


if __name__ == "__main__":
    app.run(debug=True)
