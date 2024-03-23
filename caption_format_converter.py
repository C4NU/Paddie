from PIL.ExifTags import TAGS
from model_name_mapper import ModelNameMapper
import re

class CaptionFormatConverter():
    dump_data = "NONEDATA"

    exif_dic = {
        "{body}": (272, "Camera Name"),
        "{lens}": (42036, "Lens Name 12-345mm f/6.7"),
        "{focal_f}": (41989, 51),
        "{aper}": (33437, 5.6),
        "{iso}": (34855, 100),
        "{ss}": (33434, 0.01),
        "{mf}": (271, "Camera Maker"),
        "{mf_l}": (42035, "Lens Maker"),
        "{focal}": (37386, 34),
        "{ev}": (37380, 1.33),
        "{meter}": (37383, 1),
        "{mode}": (34850, 3),
        "{time}": (36867, "1972:11:21 16:16:16"),
        "{cr}": (33432, "Copyrigth (C) Text here"),
        "{ar}": (315, "Artist Name"),
        "{wb}": (65102, "White Balance"),

        #3.2.1
        "{mode_s}": (34850, 3), # M A S P
        "{mode_cr}": (34850, 3), # M Av Tv P
    }
    
    @staticmethod
    def convert(text:str, exif_data=None, auto_hide_nonedata=False) -> str:
        exif_actual_dic = {}

        try:
            for key in list(CaptionFormatConverter.exif_dic.keys()):
                if key in exif_actual_dic: continue
                if key in text:
                    exif_actual_dic[key] = CaptionFormatConverter.get_value_in_key(key, exif_data)

            text_replaced = text
            for key in list(exif_actual_dic.keys()):
                value = exif_actual_dic[key]
                text_replaced = text_replaced.replace(key, value)

            if auto_hide_nonedata:
                # this regex represents:
                # (spaces)(one character)(spaces)NONEDATA or NONEDATA(spaces)(one character)(spaces)
                pattern = rf'((\s.{"{1}"}\s){CaptionFormatConverter.dump_data})|({CaptionFormatConverter.dump_data}(\s.{"{1}"}\s))'
                text_replaced = re.sub(pattern, '', text_replaced)
        except Exception as e:
            print(e)
            print("데이터 불량, 콘솔 창의 기록을 댓글로 남겨주세요.")
            text_replaced = text

        return text_replaced
    
    def convert_easymode(one_line:bool, exif_data=None) -> str:
        try:
            body_value = CaptionFormatConverter.get_value_in_key("{body}", exif_data)
            format_text = body_value

            # on iPhone or Galaxy: do not show lens data
            if "iPhone" in body_value or "Galaxy" in body_value:
                lens_value = CaptionFormatConverter.dump_data
            else:
                lens_value = CaptionFormatConverter.get_value_in_key("{lens}", exif_data)
            
            if lens_value != CaptionFormatConverter.dump_data:
                format_text += " | " + lens_value

            if one_line: format_text += " | "
            else: format_text += "\n"

            focal_value = CaptionFormatConverter.get_value_in_key("{focal_f}", exif_data)
            aperture_value = CaptionFormatConverter.get_value_in_key("{aper}", exif_data)
            iso_value = CaptionFormatConverter.get_value_in_key("{iso}", exif_data)
            ss_value = CaptionFormatConverter.get_value_in_key("{ss}", exif_data)

            format_text += f"{focal_value} | {aperture_value} | {iso_value} | {ss_value}"
            return format_text
        
        except Exception as e:
            print(e)
            print("데이터 불량, 콘솔 창의 기록을 댓글로 남겨주세요.")
            return ""
        
     
    @staticmethod
    def get_value_in_key(key, exif_data) -> str:
        if key not in CaptionFormatConverter.exif_dic:
            return CaptionFormatConverter.dump_data

        values = CaptionFormatConverter.exif_dic[key]
        value = exif_data.get(values[0], CaptionFormatConverter.dump_data) if exif_data else values[1]
        if value == CaptionFormatConverter.dump_data:
            if 'focal' in key:
                print(f'try exception handle canon aps-c to ff eqv focal length')
                manufacturer_info = CaptionFormatConverter.exif_dic['{mf}']
                manufacturer = exif_data.get(manufacturer_info[0], CaptionFormatConverter.dump_data)
                if manufacturer and 'Canon' in manufacturer:
                    focal_info = CaptionFormatConverter.exif_dic['{focal}']
                    value = exif_data.get(focal_info[0], CaptionFormatConverter.dump_data)
                    value *= 1.6
            elif exif_data:
                print("[" + key + "]: value not found")
                return value

        result = str(value)
        if key == "{body}": result = CaptionFormatConverter.get_body_text(value)
        if "focal" in key: result = CaptionFormatConverter.get_focal_text(value)
        if key == "{aper}": result = CaptionFormatConverter.get_aperture_text(value)
        if key == "{iso}": result = CaptionFormatConverter.get_iso_text(value)
        if key == "{ss}": result = CaptionFormatConverter.get_shutterspeed_text(value)
        if key == "{ev}": result = CaptionFormatConverter.get_exposure_text(value)
        if key == "{meter}": result = CaptionFormatConverter.get_metering_text(value)
        if key == "{mode}": result = CaptionFormatConverter.get_mode_text(value)
        if key == "{mode_s}": result = CaptionFormatConverter.get_short_mode_text(value)
        if key == "{mode_cr}": result = CaptionFormatConverter.get_canon_ricoh_mode_text(value)

        #if exif_data: print("[" + key + "]: value " + result + " found (original value: " + str(value) + ")")

        return result



    @staticmethod
    def get_body_text(body_value) -> str:
        return ModelNameMapper.replace_model_name(str(body_value))        
    
    @staticmethod
    def get_focal_text(focal_length, apsc_canon=False) -> str:
        if apsc_canon:
            focal_length *= 1.6
        return str(int(round(focal_length))) + "mm"
    
    @staticmethod
    def get_aperture_text(aperture) -> str:
        return "F/{:.1f}".format(float(aperture))
    
    @staticmethod
    def get_iso_text(iso) -> str:
        return "ISO " + str(iso)
    
    @staticmethod
    def get_shutterspeed_text(ss) -> str:
        # note(bfs): based on camera's notation format (~1/4, 0.3")
        if ss < 0.3:
            # note(komastar) : 1/1000s, 1/4000s ...
            return f'1/{int(round(1.0 / ss))}s'
        # note(komastar) : 1.0s, 30.0s ...
        return f'{round(float(ss), 1)}s'

    @staticmethod
    def get_exposure_text(exposure_value) -> str:
        str = "{:.1f}".format(float(exposure_value))
        if exposure_value > 0: str = "+" + str
        return str + " ev"
    
    @staticmethod
    def get_metering_text(metering_value) -> str:
        val = CaptionFormatConverter.dump_data
        if metering_value == 1: val = "Average"
        elif metering_value == 2: val = "Center-weighted"
        elif metering_value == 3: val = "Spot"
        elif metering_value == 4: val = "Multi-spot"
        elif metering_value == 5: val = "Multi-segment"
        elif metering_value == 6: val = "Partial"

        return val
    
    @staticmethod
    def get_mode_text(mode_value) -> str:
        if mode_value == 5: return "Slow Speed"
        if mode_value == 6: return "High Speed"
        if mode_value == 7: return "Portrait"
        if mode_value == 8: return "Landscape"
        
        if mode_value <= 0 or mode_value > 8: return CaptionFormatConverter.dump_data

        if mode_value == 1: return "Manual"
        if mode_value == 2: return "Program"
        if mode_value == 3: return "Aperture Priority"
        if mode_value == 4: return "Shutter Speed Priority"

        return CaptionFormatConverter.dump_data
    
    @staticmethod
    def get_short_mode_text(mode_value) -> str:
        if mode_value == 1: return "M"
        if mode_value == 2: return "P"
        if mode_value == 3: return "A"
        if mode_value == 4: return "S"

        return CaptionFormatConverter.dump_data
    
    @staticmethod
    def get_canon_ricoh_mode_text(mode_value) -> str:
        if mode_value == 1: return "M"
        if mode_value == 2: return "P"
        if mode_value == 3: return "Av"
        if mode_value == 4: return "Tv"

        return CaptionFormatConverter.dump_data

