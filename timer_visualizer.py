from PIL import Image, ImageDraw, ImageFont
from myoled import MyOled
import cv2

class Visualizer:
    def __init__(self):
        self.oled = MyOled()
        self.font = ImageFont.truetype('fonts/Perfect DOS VGA 437.ttf', 32)
        
        with Image.open("images/hev.bmp") as img:
            img = img.convert("1")
            self.img = Image.eval(img, lambda x: 255 - x)

    def refresh(self, text, loading_bar_value=0.0):
        image = Image.new("1", (self.oled.width, self.oled.height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Draw a white background
        bar_height = 10
        #draw.rectangle((0, self.oled.height-bar_height, int(self.oled.width * percentage), self.oled.height), outline=255, fill=255)
        draw.bitmap((-4 - int(128*(1-loading_bar_value)), self.oled.height-bar_height), self.img, fill=255)

        # Draw Some Text
        (font_width, font_height) = self.font.getsize(text)
        draw.text(
            (self.oled.width // 2 - font_width // 2, self.oled.height // 2 - font_height // 2),
            text,
            font=self.font,
            fill=255,
            size=1,
        )

        # Display image
        self.oled.image(image)

        self.oled.show()
        
