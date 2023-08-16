from PIL import Image

import os

class Converter():
	def __init__(self) -> None:
		pass

	def ConvertImage(self, filePath, savePath):
		# 확장자명 탐색
		condition, fileFormat = self.SearchFileFormat(filePath)

		if(condition):
			# jpg, jpeg, png, tiff 등 지원하는 파일 형식일 때
			image = Image.open(filePath).convert("RGB")
			filePath = filePath.replace(fileFormat, '.webp')
			image.save(savePath+".webp", "webp")
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