from MockupEngineer import MockupEngineerInstance
from PIL import Image

mockup = MockupEngineerInstance()


def get_image_mokeup(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
    if width >= height:
        q = mockup.generate(
            template_id="4724b1349442f7fdaa60216d31cbd6a8",
            screenshot_path=image_path,
            color=mockup.templates[0].colors[0].color,
        )
    else:
        q = mockup.generate(
            template_id=mockup.templates[0].id,
            screenshot_path=image_path,
            color=mockup.templates[0].colors[0].color,
        )
    return q
