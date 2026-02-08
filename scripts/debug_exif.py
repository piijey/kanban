from pillow_heif import register_heif_opener
from PIL import Image

register_heif_opener()

img = Image.open("data_raw-img/IMG_9358.HEIC")
img.save("IMG_9358.jpg", "JPEG", exif=img.getexif())  # exif引数で明示的に保存


from xlsx2json import get_image_metadata
metadata = get_image_metadata("IMG_9358.jpg")
print(metadata)
