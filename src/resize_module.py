from PIL import Image

class Resize:
	def __init__(self):
		pass

	def resize(self, image, axis_option, resize):
		width, height = image.size

		width_option = True
		if axis_option == 0: width_option = True
		elif axis_option == 1: width_option = False
		elif axis_option == 2: width_option = width >= height
		elif axis_option == 3: width_option = width < height

		if width_option == True:
			new_width = resize
			new_height = new_width * height / width
		else:
			new_height = resize
			new_width = new_height * width / height

		image = image.resize((int(new_width), int(new_height)), Image.LANCZOS)

		return image