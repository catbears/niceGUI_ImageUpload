import base64
import io
from time import sleep

from nicegui import ui
from nicegui.events import UploadEventArguments
from PIL import Image


# Helper functions
def check_upload(file_name: str, folder_name: str) -> bool:
    """
    Check if the file exists in that location

    We use this to check if the upload has worked

    :param folder_name: folder where the upload is saved
    :param file_name: Is the file name
    :return: True if the file exists, False otherwise
    """

    try:
        im = Image.open(f"./{folder_name}/{file_name}")
        return True

    except (OSError, FileNotFoundError, ValueError):
        return False


# Todo: Clean up the encoding and decoding of the image
def handle_upload(e: UploadEventArguments) -> None:
    """
    Handle the upload event for uploading an image

    :param e: Is the event arguments
    :return: None
    """

    name = e.name
    content = e.content

    # We read the content of the file and encode it to base64, because NiceGUI doesn't support binary data
    image = io.BytesIO(content.read())
    encoded_string = base64.b64encode(image.read()).decode()

    # We decode the base64 string to be able to save it as an image
    base64_string = encoded_string
    image_bytes = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_bytes))

    # We save the image to the uploads folder
    container = ui.row()

    try:
        image.save(f"./uploads/{name}")
    except (OSError, FileNotFoundError, ValueError):
        with container:
            ui.label("Saving failed")
            ui.icon("thumb_down").style("color: #cd1608")

    if check_upload(name, "uploads"):
        with container:
            ui.label("Upload successful")
            ui.icon("thumb_up").style("color: #30bb24")

    else:
        with container:
            ui.label("Upload failed")
            ui.icon("thumb_down").style("color: #cd1608")


@ui.page("/", title="Upload File")
def main():
    ul_return = ui.upload(on_upload=handle_upload)


ui.run()
