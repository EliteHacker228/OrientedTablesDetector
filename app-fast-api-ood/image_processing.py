from io import BytesIO
from PIL import Image


def prepare_image(image_array, format="PNG"):
    """Преобразует numpy-массив изображения в байтовый поток."""
    image_pil = Image.fromarray(image_array)
    image_bytes = BytesIO()
    image_pil.save(image_bytes, format=format)
    image_bytes.seek(0)
    return image_bytes
