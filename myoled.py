import board
import busio
import digitalio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont, ImageOps
import cv2

# SCL: SCLK
# SDA: MOSI
# RES: 4
# DC: 6

class MyOled(adafruit_ssd1306.SSD1306_SPI):
	def __init__(self):
		spi = busio.SPI(board.SCK, MOSI=board.MOSI)
		reset_pin = digitalio.DigitalInOut(board.D4) # any pin!
		cs_pin = digitalio.DigitalInOut(board.D5)    # any pin!
		dc_pin = digitalio.DigitalInOut(board.D6)    # any pin!

		super(MyOled, self).__init__(128, 64, spi, dc_pin, reset_pin, cs_pin)

	def draw_function(self,x,y,width,height,data):
		assert len(data) == width, "{}!={}".format(len(data), width)
		max_data = max(data)
		min_data = min(data)
		self.rect(x-1,y-1,width+2,height+2,0,fill=True)
		self.rect(x-1,y-1,width+2,height+2,1)
		for i in range(len(data)):
			value = int(height*(data[i] - min_data) / (max_data-min_data))
			self.pixel(x+i,y+height-value,1)
	
	def draw_image(self, image, pad_color=0):		
		im_pil = Image.fromarray(image).convert('1')
		im_pil = ImageOps.pad(im_pil, (self.width, self.height), color=pad_color)
		self.image(im_pil)
		
