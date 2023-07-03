import numpy as np
import sys
from PIL import Image, ImageDraw, ImageFont
import random

from ASCII_converter import Converter_ASCII

if __name__ == "__main__":
    conv = Converter_ASCII("imgs\mona-lisa-c-1503-1519.jpg", True)
    
    data = conv.convert_to_ASCII()

    PIXELS = 16
    reduce_size = 2
    
    w = conv.get_image_shape()[1]
    h = conv.get_image_shape()[0]

    img = Image.new("RGB", (w * PIXELS // reduce_size, h * PIXELS // reduce_size), (255, 255, 255))

    i_draw = ImageDraw.Draw(img)

    # 12pt size font equals 16px
    # 6pt - 8px
    font = ImageFont.truetype('fonts\FreeMonoBold.ttf', 12)
    
    text = "monalisa"
    
    for x, it_x in zip(data, range(len(data))):
        it_y = 0
        for y in x:
            
            curr_y = it_x * PIXELS // reduce_size
            curr_x = it_y * PIXELS // reduce_size
            
            # if conv.image[it_x][it_y][3] == 0:
            #     it_y += 1
            #     continue
            i_draw.text((curr_x, curr_y), text[random.randint(0, len(text)-1)], font = font, fill=(conv.image[it_x][it_y][0], conv.image[it_x][it_y][1], conv.image[it_x][it_y][2]))
            it_y += 1
        # i_draw.text((0,it*PIXELS), line, font = font, fill=(0,0,0))

    img.show()
    img.save("img.png")