# Copyright 2023 Hyo Jae Jeon (CANU) canu1832@gmail.com

from PIL import Image, ImageDraw, ImageFont

import os
#import Watermark_module
import Exif_module

class Converter():
	def __init__(self) -> None:
		#self.watermark = Watermark_module.Watermark()
		self.exif = Exif_module.Exif()

	def ConvertImage(self, filePath, savePath, saveName, loselessOpt, imageQualityOpt, exifOpt, iccProfileOpt, exactOpt, watermarkText, exifViewOpt, instaResizeOpt, conversionOpt):
		# 확장자명 탐색
		condition, fileFormat = self.SearchFileFormat(filePath)

		if(condition):
			image = Image.open(filePath)

			if exifViewOpt == True:
				longerLength = image.width if image.width >= image.height else image.height
				padding = int(longerLength / 10)

				modelData, exifData = self.exif.GetExifData(image)
				horizontalImage = True if image.width>=image.height else False
				if instaResizeOpt==True:
					image = self.exif.SetInstaPadding(image, gap = 40, color=(255,255,255), horizontalImage= horizontalImage)
					image = self.exif.SetInstaText(image, modelData=modelData, exifData=exifData, horizontalImage= horizontalImage)
					
				else : 
					image = self.exif.SetImagePadding2(image, top=int(padding/2), side=int(padding/2), bottom=padding, color=(255,255,255))
					image = self.exif.SetImageText(image, modelData=modelData, exifData=exifData, length = padding)
			# jpg, jpeg, png, tiff 등 지원하는 파일 형식일 때

			if conversionOpt == True:
				imageData = Image.open(filePath).convert('RGB')

				filePath = filePath.replace(fileFormat, '.webp')
				dest = savePath+saveName+".webp"
				
				exifData = getattr(imageData.info, 'exif', None)
				if not exifData:
					print(f'no exif data {saveName}')
					exifOpt = False

				iccProfile = imageData.info['icc_profile']
			
				#image = self.watermark.InsertWatermark(image=image, fontColor=watermarkColor, watermarkText=watermarkText)

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
			else:
				# webp 변환 말고 확장자 그대로
				imageData = Image.open(filePath).convert('RGB')

				filePath = filePath.replace(fileFormat, '.png')
				dest = savePath+saveName+".png"
				exifData = imageData.info['exif']
				iccProfile = imageData.info['icc_profile']
			
				#image = self.watermark.InsertWatermark(image=image, fontColor=watermarkColor, watermarkText=watermarkText)

				if exifOpt == True:
					if iccProfileOpt == True:
						image.save(dest, format="png", loseless=loselessOpt, quality=imageQualityOpt, exif=exifData, exact = exactOpt, icc_profile=iccProfile)
					else:
						image.save(dest, format="png", loseless=loselessOpt, quality=imageQualityOpt, exif=exifData, exact = exactOpt)

				else:
					if iccProfileOpt == True:
						image.save(dest, format="png", loseless=loselessOpt, quality=imageQualityOpt, exact=exactOpt, icc_profile=iccProfile)
					else:
						image.save(dest, format="png", loseless=loselessOpt, quality=imageQualityOpt, exact=exactOpt)


	def SearchFileFormat(self, filePath):
		fileFormat = os.path.splitext(filePath)[1]
		if(fileFormat == ".jpg" or fileFormat == ".jpeg" or fileFormat == ".png" or fileFormat == ".tiff"):
			return True, fileFormat
		else:
			return False, None