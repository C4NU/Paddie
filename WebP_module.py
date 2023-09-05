# Copyright 2023 Hyo Jae Jeon (CANU) canu1832@gmail.com

from PIL import Image, ImageDraw, ImageFont

import os
import Watermark_module
import Exif_module

class Converter():
	def __init__(self) -> None:
		self.watermark = Watermark_module.Watermark()
		self.exif = Exif_module.Exif()

	def ConvertImage(self, filePath, savePath, saveName, loselessOpt, imageQualityOpt, exifOpt, iccProfileOpt, exactOpt, watermarkText, exifViewOpt):
		# 확장자명 탐색
		condition, fileFormat = self.SearchFileFormat(filePath)

		if(condition):
			image = Image.open(filePath)

			if exifViewOpt == True:
				longerLength = image.width if image.width >= image.height else image.height
				padding = int(longerLength / 10)

				modelData, exifData = self.exif.GetExifData(image)
				image = self.exif.SetImagePadding2(image, top=int(padding/2), side=int(padding/2), bottom=padding, color=(255,255,255))
				image = self.exif.SetImageText(image, modelData=modelData, exifData=exifData, length = padding)
			# jpg, jpeg, png, tiff 등 지원하는 파일 형식일 때

			imageData = Image.open(filePath).convert('RGB')

			filePath = filePath.replace(fileFormat, '.webp')
			dest = savePath+saveName+".webp"
			exifData = imageData.info['exif']
			iccProfile = imageData.info['icc_profile']
			
			#image = self.watermark.InsertWatermark(image=image, fontColor=watermarkColor, watermarkText=watermarkText)
			print(exifOpt)
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

			print("변환 완료 되었습니다.")
		else:
			# 지원하지 않는 파일 형식일 때
			print("지원하지 않는 파일 형식 입니다.")

	def SearchFileFormat(self, filePath):
		fileFormat = os.path.splitext(filePath)[1]
		if(fileFormat == ".jpg" or fileFormat == ".jpeg" or fileFormat == ".png" or fileFormat == ".tiff"):
			return True, fileFormat
		else:
			return False, None