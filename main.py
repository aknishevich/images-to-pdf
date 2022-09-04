import os
import sys

from fpdf import FPDF
from pathlib import Path
from PIL import Image

if __name__ == '__main__':
    valid_images = [".jpg", ".gif", ".png", ".tga"]
    pdf = FPDF()

    current_directory = os.getcwd()
    directory_separator = os.sep

    path_where_to_store = current_directory + directory_separator + "result"
    path_to_images = current_directory + directory_separator + "img"
    pdf_name = "result"

    Path(path_where_to_store).mkdir(parents=True, exist_ok=True)

    if len(sys.argv) == 2:
        path_to_images = sys.argv[1]
    elif len(sys.argv) == 3:
        path_to_images = sys.argv[1]
        path_where_to_store = sys.argv[2]
    elif len(sys.argv) == 4:
        path_to_images = sys.argv[1]
        path_where_to_store = sys.argv[2]
        pdf_name = sys.argv[3]

    for file_name in os.listdir(path_to_images):
        ext = os.path.splitext(file_name)[1]

        if ext.lower() not in valid_images:
            continue

        cover = Image.open(path_to_images + directory_separator + file_name)
        width, height = cover.size

        # convert pixel in mm with 1px=0.264583 mm
        width, height = float(width * 0.264583), float(height * 0.264583)

        # A4 format size
        pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}

        # get page orientation from image size
        orientation = 'P' if width < height else 'L'

        #  make sure image size is not greater than the pdf format size
        width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
        height = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']

        pdf.add_page(orientation=orientation)

        pdf.image(path_to_images + directory_separator + file_name, 0, 0, width, height)

    result_file_path = path_where_to_store + directory_separator + pdf_name + ".pdf"

    pdf.output(result_file_path, "F")
