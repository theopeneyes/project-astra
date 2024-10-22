from io import BytesIO 
import PIL 
import base64 

def encode_image(image: PIL.Image) -> str: 
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")
