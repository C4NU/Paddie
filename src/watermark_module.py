from PIL import Image, ImageFont, ImageDraw

import os, platform

class Watermark():
	def __init__(self):
		# 변수 초기화

		# 폰트 사이즈 (초기)
		self.fontSize = 30
		# 폰트 (초기)
		if platform.system() == "Windows":
			self.font = ImageFont.truetype(os.path.join(os.getcwd(), '../resources/Barlow-Light.ttf'), self.font_size)
		else:
			try:
				self.font = ImageFont.truetype(os.path.join(os.path.dirname(sys.executable), "../resources/Barlow-Light.ttf"), self.font_size)
			except:
				self.font = ImageFont.truetype(os.path.join(os.getcwd(), '../resources/Barlow-Light.ttf'), self.font_size)

	def insert_watermark(self, image, fontColor, watermarkText):
			width, height = image.size

			draw = ImageDraw.Draw(image)
			x, y = int(width/2), int(height/2)

			self.font = ImageFont.truetype("Barlow-Light.ttf", self.fontSize)

			if fontColor:	# FontColor가 
				draw.text(xy=(width / 2 - (self.fontSize * 2), height / 2), text = watermarkText,font=self.font, fill=(0,0,0))
			else:
				draw.text(xy=(width / 2 + (self.fontSize * 2), height / 2), text = watermarkText, font = self.font, fill = (255,255,255))

			return image

	def set_font_size(self, x, y):
		if x > y:
			self.fontSize = y
		elif y > x:
			self.fontSize = x
		else:
			self.fontSize = x

		self.fontSize = int(self.fontSize/6)

	def steganography(self, image, watermarkText):
		'''
		이미지 파일에 저작권 요소를 삽입하는 함수
		사용자 이름 / 이메일 등등 데이터 삽입
		'''
		
		pass

if __name__ == "__main__":
	test_image = Image.open("../resources/test/sample.jpg")
	watermark_test = Watermark()

	# 워터마크 삽입 기능 테스트
	# 스테가노그래피 기능 테스트
