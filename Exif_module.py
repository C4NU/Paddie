# Copyright 2023 Hyo Jae Jeon (CANU) canu1832@gmail.com

from PIL import Image, ImageDraw, ImageFont

# 폰트 vs padding 비율은 1:4?
# 이미지파일 vs padding 비율은 10:1
class Exif():
	def __init__(self):
		# 폰트 사이즈 (초기)
		self.fontSize = 50
		# 폰트 (초기)
		self.font = ImageFont.truetype("./Resources/Fonts/Barlow/Barlow-Light.ttf", self.fontSize)

	def GetExifData(self, image):
		exifData = image._getexif()
		
		if exifData is None:
			print('Sorry, image has no exif data.')
		else:
			model = str(exifData[272]) if 272 in exifData else None
			lensModel = str(exifData[42036]) if 42036 in exifData else None
			fNumber = str(exifData[33437]) if 33437 in exifData else None
			focalLength = str(exifData[41989]) if 41989 in exifData else None
			iso = str(exifData[34855]) if 34855 in exifData else None
			
			try:
				shutterSpeedValue = 1 / (2 ** exifData[37377])
				shutterSpeed = f"1/{int(round(1/shutterSpeedValue))}s"
			
			except KeyError:
				pass

			if lensModel is None:
				resultModel = model
			else:
				resultModel = model + " | " + lensModel

			if focalLength is None:
				focalLength = exifData[37386]
				
				if model.find("X100") != -1:
					focalLength = round(focalLength * 1.5 + 0.1)
					focalLength = str(focalLength)
			else:
				pass

			resultExif = focalLength + "mm | F/" + fNumber + " | " + "ISO " + iso + " | " + shutterSpeed

			print(resultExif)

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
		self.font = ImageFont.truetype("./Resources/Fonts/Barlow/Barlow-Light.ttf", self.fontSize)

		draw.text(xy = (x,y - self.fontSize / 2), text = modelData,font=self.font, fill=(0,0,0), anchor="ms")
		draw.text(xy = (x,y + self.fontSize), text = exifData,font=self.font, fill=(0,0,0), anchor="ms")
		
		return image
	
def main():
	exifTest = Exif()

	img = Image.open("DSCF4365.jpg")

	longerLength = img.width if img.width >= img.height else img.height
	padding = int(longerLength / 10)\
	

	modelData, exifData = exifTest.GetExifData(img)
	img = exifTest.SetImagePadding2(img, top=int(padding/2), side=int(padding/2), bottom=padding, color=(255,255,255))
	img = exifTest.SetImageText(img, modelData=modelData, exifData=exifData, length = padding)
	img.show()
	

if __name__=="__main__":
	main()