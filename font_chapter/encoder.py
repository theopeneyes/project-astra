import base64
import io 

def encode_image(image) -> str:
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return encoded_image