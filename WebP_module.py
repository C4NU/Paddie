from PIL import Image, ImageDraw, ImageFont

import os
import Watermark_module

class Converter():
	def __init__(self) -> None:
		self.watermark = Watermark_module.Watermark()

	def ConvertImage(self, filePath, savePath, saveName, loselessOpt, imageQualityOpt, exifOpt, iccProfileOpt, exactOpt, watermarkText):
		# 확장자명 탐색
		condition, fileFormat = self.SearchFileFormat(filePath)

		if(condition):
			# jpg, jpeg, png, tiff 등 지원하는 파일 형식일 때
			image = Image.open(filePath).convert("RGB")
			image = self.watermark.InsertWatermark(image, watermarkText)

			filePath = filePath.replace(fileFormat, '.webp')
			dest = savePath+saveName+".webp"
			exif = image.info['exif']
			iccProfile = image.info['icc_profile']
			
			if exifOpt == True:
				if iccProfileOpt == True:
					image.save(dest, format="webp", loseless=loselessOpt, quality=imageQualityOpt, exif=exif, exact = exactOpt, icc_profile=iccProfile)
				else:
					image.save(dest, format="webp", loseless=loselessOpt, quality=imageQualityOpt, exif=exif, exact = exactOpt)

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