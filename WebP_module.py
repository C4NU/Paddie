from PIL import Image

class Converter():
	#ConvertImage에서 처리
	def __init__(self) -> None:
		pass

	def ConvertImage(filePath = "file Path"):
		image = Image.open(filePath).convert("RGB")
		filePath = filePath[:-4]	# TO FIX: 마지막 파일 확장자명만 떼네는 방법 생각하기
		image.save(filePath+".webp", "webp")