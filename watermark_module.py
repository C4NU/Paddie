from PIL import Image, ImageFont, ImageDraw

import os, platform

class Watermark():
	def __init__(self):
		# 변수 초기화

		# 폰트 사이즈 (초기
		self.fontSize = 30
		# 폰트 (초기)
		self.font = ImageFont.truetype("Barlow-Light.ttf", self.fontSize)

	def InsertWatermark(self, image, fontColor, watermarkText):
			width, height = image.size

			draw = ImageDraw.Draw(image)
			x, y = int(width/2), int(height/2)

			self.font = ImageFont.truetype("Barlow-Light.ttf", self.fontSize)

			if fontColor:	# FontColor가 
				draw.text(xy=(width / 2 - (self.fontSize * 2), height / 2), text = watermarkText,font=self.font, fill=(0,0,0))
			else:
				draw.text(xy=(width / 2 + (self.fontSize * 2), height / 2), text = watermarkText, font = self.font, fill = (255,255,255))

			return image

	def SetFontSize(self, x, y):
		if x > y:
			self.fontSize = y
		elif y > x:
			self.fontSize = x
		else:
			self.fontSize = x

		self.fontSize = int(self.fontSize/6)

