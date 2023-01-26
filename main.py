import base64
import io

from nicegui import ui
from nicegui.events import UploadEventArguments
from PIL import Image


# Todo: Clean up the encoding and decoding of the image
def handle_upload(e: UploadEventArguments) -> None:
    """
    Handle the upload event for uploading an image

    :param e: Is the event arguments
    :return: None
    """

    name = e.name  # not used, kept for reference
    content = e.content

    # We read the content of the file and encode it to base64, because NiceGUI doesn't support binary data
    image = io.BytesIO(content.read())
    encoded_string = base64.b64encode(image.read()).decode()

    # We add the data:image/png;base64, prefix to the encoded string, so nicegui knows it's an image
    image_base64 = "data:image/png;base64," + encoded_string
    # ui.image(image_base64) # Uncomment this line to see the image in the browser

    # We decode the base64 string to be able to save it as an image
    base64_string = encoded_string
    image_bytes = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_bytes))
    image.save(f"./uploads/{name}")


@ui.page("/", title="Upload File")
def main():
    ui.upload(on_upload=handle_upload)


ui.run()
