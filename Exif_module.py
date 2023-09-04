# Copyright 2023 Hyo Jae Jeon (CANU) canu1832@gmail.com

from PIL import Image, ImageDraw, ImageFont

# 폰트 vs padding 비율은 1:4?
# 이미지파일 vs padding 비율은 10:1
class Exif():
	def __init__(self):
		# 폰트 사이즈 (초기)
		self.fontSize = 50
		# 폰트 (초기)
		self.font = ImageFont.truetype("./Resources/Fonts/Poppins/Poppins-Light.ttf", self.fontSize)

	def GetExifData(self, image):
		exifData = image._getexif()
		
		if exifData is None:
			print('Sorry, image has no exif data.')
		else:
			model = str(exifData[272])
			lensModel = str(exifData[42036])
			fNumber = str(exifData[33437])
			focalLength = str(exifData[41989])
			iso = str(exifData[34855])
			
			shutterSpeedValue = 1 / (2 ** exifData[37377])
			shutterSpeed = f"1/{int(round(1/shutterSpeedValue))}s"

			resultModel = model + " | " + lensModel
			resultExif = focalLength + "mm | F/" + fNumber + " | " + "ISO " + iso + " | " + shutterSpeed

			return resultModel, resultExif

	def SetImagePadding(self, image, length, color):
		width, height = image.size
		new_width = width + 2*length
		new_height = height + 2*length
		
		result = Image.new(image.mode, (new_width, new_height), color)
		result.paste(image, (length, length))

		return result
	
	def SetImagePadding2(self, image, top, side, bottom, color):
		width, height = image.size

		newWidth = width + 2*side
		newHeight = height + 2 + top + bottom
		
		result = Image.new(image.mode, (newWidth, newHeight), color)
		result.paste(image, (side, top))

		return result
	
	def SetImageText(self, image, modelData, exifData, length):
		draw = ImageDraw.Draw(image)
		x = image.width / 2
		y = image.height - (length / 2)

		self.fontSize = length / 4.5
		self.font = ImageFont.truetype("./Resources/Fonts/Poppins/Poppins-Light.ttf", self.fontSize)

		draw.text(xy = (x,y - self.fontSize / 2), text = modelData,font=self.font, fill=(0,0,0), anchor="ms")
		draw.text(xy = (x,y + self.fontSize), text = exifData,font=self.font, fill=(0,0,0), anchor="ms")
		
		return image
	
def main():
	exifTest = Exif()

	img = Image.open("P8302280.jpg")
	padding = int(img.width / 10)

	modelData, exifData = exifTest.GetExifData(img)
	img = exifTest.SetImagePadding2(img, top=int(padding/2), side=int(padding/2), bottom=padding, color=(255,255,255))
	img = exifTest.SetImageText(img, modelData=modelData, exifData=exifData, length = padding)
	img.show()

	img.save("04.jpg")
	

if __name__=="__main__":
	main()