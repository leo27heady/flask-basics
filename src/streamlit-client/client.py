import os
import requests
import json

import streamlit as st


def title_write():
    st.title("Image classification")


def image_uploader():
    uploaded_image = st.file_uploader(
        label="Choose image",
        type=("png", "jpg", "jpeg"),
        accept_multiple_files=False,
    )
    return uploaded_image


def classify_image(uploaded_image, server_url):
    data = uploaded_image.read()
    image_path = os.path.join(os.path.dirname(__file__), uploaded_image.name)
    f = open(image_path, "wb")
    f.write(data)
    f.close()

    send_image = open(image_path, "rb")
    files = {"file": send_image}

    r = requests.post(server_url, files=files)
    send_image.close()
    os.remove(image_path)

    predict = json.loads(r.content.decode("utf-8"))
    return predict


def screen_predict(predict):
    st.write(
        """
    ## Image `{}` class: `{}`
    """.format(
            predict["image_name"], predict["class_id"]
        )
    )


if __name__ == "__main__":
    server_url = "http://localhost:5000/uploader"

    title_write()
    uploaded_image = image_uploader()

    if uploaded_image is not None:
        predict = classify_image(uploaded_image, server_url)
        screen_predict(predict)
