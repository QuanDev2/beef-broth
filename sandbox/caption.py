import base64
from pathlib import Path
from llm import call_llm

HERE = Path(__file__).parent          # the folder caption.py lives in
image_bytes = (HERE / "photos" / "saigon-1.webp").read_bytes()
image_data = base64.standard_b64encode(image_bytes).decode("utf-8")

message = [{
    "role": "user",
    "content": [
        {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/webp",
                "data": image_data,
            },
        },
        {"type": "text", "text": "Describe this photo."},
    ],
}]


print(call_llm(message))
