from PIL import Image, ImageFont, ImageDraw

class Watermark():
	def __init__(self):
		# 변수 초기화

		# 폰트 사이즈 (초기)
		self.fontSize = 30
		# 폰트 (초기)
		self.font = ImageFont.truetype("arial.ttf", self.fontSize)

	def InsertWatermark(self, image, watermarkText):
			width, height = image.size

			draw = ImageDraw.Draw(image)
			x, y = int(width/2), int(height/2)

			if x > y:
				fontSize = y
			elif y > x:
				fontSize = x
			else:
				fontSize = x

			fontSize = int(fontSize/6)
			font = ImageFont.truetype("arial.ttf", fontSize)

			draw.text(xy=(width / 2 - (fontSize * 2), height / 2), text = watermarkText,font=font, fill=(0,0,0))
			draw.text(xy=(width / 2 + (fontSize * 2), height / 2), text = watermarkText, font = font, fill = (255,255,255))

			return image


