75mm | F/2.8 | ISO 640 | 1/125s
no exif data 01
Traceback (most recent call last):
  File "C:\Users\canu1\Documents\Development\#1 Python Projects\WebPConverterGUI\main.py", line 102, in okButtonClicked
    self.SaveFile()
  File "C:\Users\canu1\Documents\Development\#1 Python Projects\WebPConverterGUI\main.py", line 144, in SaveFile
    self.converter.ConvertImage(self.listWidget.item(index).text(), strSavePath+'/',
  File "C:\Users\canu1\Documents\Development\#1 Python Projects\WebPConverterGUI\WebP_module.py", line 47, in ConvertImage
    image.save(dest, format="webp", loseless=loselessOpt, quality=imageQualityOpt, exif=exifData, exact = exactOpt)
  File "C:\Users\canu1\AppData\Local\Programs\Python\Python310\lib\site-packages\PIL\Image.py", line 2413, in save
    save_handler(self, fp, filename)
  File "C:\Users\canu1\AppData\Local\Programs\Python\Python310\lib\site-packages\PIL\WebPImagePlugin.py", line 326, in _save
    if exif.startswith(b"Exif\x00\x00"):
AttributeError: 'NoneType' object has no attribute 'startswith'

no exif data로 pass 들어가는데 그러면 exifdata가 없는상태로 호출을 하니까 당연히 안돌아감

근데 이미지 파일에는 exif 데이터가 있음???????????