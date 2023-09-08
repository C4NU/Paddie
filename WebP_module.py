# Copyright 2023 Hyo Jae Jeon (CANU) canu1832@gmail.com

from PIL import Image, ImageDraw, ImageFont, ImageOps, ExifTags

import os
#import Watermark_module
import Exif_module

class Converter():
	def __init__(self) -> None:
		#self.watermark = Watermark_module.Watermark()
		self.exif = Exif_module.Exif()

	def FixOrientation(self, image):
		exif = image._getexif()
		try:
			if exif:
				orientation = exif.get(274)

				if orientation == 3:
					new_image = image.rotate(180, expand=True)
				elif orientation == 6:
					new_image = image.rotate(270, expand=True)
				elif orientation == 8:
					new_image = image.rotate(90, expand=True)
				
				new_image.info = image.info()
		except Exception as e:
			print(e)
	
		return new_image

	def ConvertImageToWebP(self, filePath, savePath, saveName, loselessOpt, imageQualityOpt, exifOpt, iccProfileOpt, exactOpt, watermarkText, exifViewOpt, conversionOpt):
		condition, fileFormat = self.SearchFileFormat(filePath)

		if condition:
			# 01 일반 WebP 형식 Image로 변환할 때
			if conversionOpt == True:
				image = Image.open(filePath).convert("RGB")
				#image = self.FixOrientation(image)

				filePath = filePath.replace(fileFormat, '.webp')
				dest = savePath+saveName+".webp"
				
				# 여기서 exif 데이터의 특정 값이 존재하지 않으면 바로 실패함 / 옵션을 선택하지 않아도 읽어오기에 무조건적으로 뻗음
				#exifData = getattr(image.info, 'exif', None)
				#if not exifData:
				#	print(f'no exif data {saveName}')
				#	exifOpt = False
				exifOpt = False

				iccProfile = image.info['icc_profile']
			
				#image = self.watermark.InsertWatermark(image=image, fontColor=watermarkColor, watermarkText=watermarkText)

				image = image.convert("RGB")

				if exifOpt == True:
					if iccProfileOpt == True:
						image.save(dest, format="webp", loseless=loselessOpt, quality=imageQualityOpt, exif=exifData, exact = exactOpt, icc_profile=iccProfile)
					else:
						image.save(dest, format="webp", loseless=loselessOpt, quality=imageQualityOpt, exif=exifData, exact = exactOpt)

				else:
					if iccProfileOpt == True:
						image.save(dest, format="webp", loseless=loselessOpt, quality=imageQualityOpt, exact=exactOpt, icc_profile=iccProfile)
					else:
						image.save(dest, format="webp", loseless=loselessOpt, quality=imageQualityOpt, exact=exactOpt)

	def ConvertExifImage(self, filePath, savePath, saveName, fileFormatOpt):
		condition, fileFormat = self.SearchFileFormat(filePath)

		if condition:
			# 02 EXIF Padding Image로 변환할 때
			image = Image.open(filePath)

			longerLength = image.width if image.width >= image.height else image.height
			padding = int(longerLength / 10)

			modelData, exifData = self.exif.GetExifData(image)

			image = self.FixOrientation(image)

			image = self.exif.SetImagePadding2(image, top=int(padding/2), side=int(padding/2), bottom=padding, color=(255,255,255))
			image = self.exif.SetImageText(image, modelData=modelData, exifData=exifData, length = padding)

			# 파일 형식 선택
			if fileFormatOpt == 0:
				dest = savePath+saveName+'.jpeg'
				image.save(dest, format='jpeg')
			elif fileFormatOpt == 1:
				dest = savePath+saveName+'.png'
				image.save(dest, format='png')
			elif fileFormatOpt == 2:
				dest = savePath+saveName+'.webp'
				image.save(dest, format='webp', quality=92)
			else:
				print("잘못된 파일 변환 선택지 입니다.")
				return

		else:
			print("잘못된 파일 형식 입니다.")
			return

	def SearchFileFormat(self, filePath):
		fileFormat = os.path.splitext(filePath)[1]
		fileFormat = fileFormat.lower()

		if(fileFormat == ".jpg" or fileFormat == ".jpeg" or fileFormat == ".png" or fileFormat == ".tiff" or fileFormat == ".webp"):
			return True, fileFormat
		else:
			return False, None