from PIL import Image, ImageDraw, ImageFont
import time
import string
import random
from .import config


def create_default_captcha_image():
    """
    returns new white background PIL.Image of 150x50
    """
    image = Image.new('RGB',(150,50), (255,255,255))
    return image


def generate_captcha_code():
    """
    returns random code containing upper/lower alphabets, numbers, @!$# letters
    """
    letters = string.ascii_letters
    ctime = "".join(str(time.time()).split("."))
    other_letters = "@!$#"
    mixing = letters+ctime+other_letters
    captcha_code = "".join(random.choice(mixing) for _ in range(6))
    return captcha_code


def draw_captcha_on_image(captcha_code, image):
    """
    draw text on image
    """
    image_draw = ImageDraw.Draw(image)

    padding_left = 20
    padding_top = 8

    i = 1
    for letter in captcha_code:
        if i%3 == 0:
            color_fill = (0, 0, random.randint(0,180))
        elif i%2 == 0:
            color_fill = (0, random.randint(0,180), 0)
        else:
            color_fill = (random.randint(0,180), 0, 0)
        i += 1

        padding_top = random.randint(4,10)

        image_draw.text((padding_left, padding_top), letter, fill=color_fill, font=ImageFont.truetype(config.FONT_FILE ,config.FONT_SIZE))
        padding_left += 18

    for _ in range(2):
        image_draw.line(
            (
                random.randint(10,40), random.randint(10,40),
                random.randint(110,140), random.randint(10, 40),
            ),
            fill=(random.randint(0,150), random.randint(0,150), random.randint(0,150)),
            width=random.randint(3,4)
        ), #type:ignore

    for _ in range(2):
        image_draw.line(
            random.choice(
                [
                    (
                        random.randint(10, 70), random.randint(0,10),
                        random.randint(10, 70), random.randint(40,50),
                    ),
                    (
                        random.randint(80, 140), random.randint(0,10),
                        random.randint(80, 140), random.randint(40,50),
                    ),
                ]
            )
            ,
            fill=(random.randint(0,150), random.randint(0,150), random.randint(0,150)),
            width=2
        )