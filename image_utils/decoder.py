from io import BytesIO 
import PIL 
import base64 

def decode_image(encoded_string: str) -> PIL.Image.Image:
    image_data = base64.b64decode(encoded_string)
    buffered = BytesIO(image_data)
    image = PIL.Image.open(buffered)
    return image