import os
from PyQt6.QtCore import QThread, pyqtSignal

class ConversionWorker(QThread):
    progress = pyqtSignal(int)
    finished_conversion = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, mode, file_paths, file_names, save_path, config_options, font_path=""):
        super().__init__()
        self.mode = mode
        self.file_paths = file_paths
        self.file_names = file_names
        self.save_path = save_path
        self.config_options = config_options
        self.font_path = font_path

    def run(self):
        try:
            import converter.convert_module as convert_module
            conv = convert_module.Converter()
            total_files = len(self.file_paths)
            
            for index, (file_path, file_name) in enumerate(zip(self.file_paths, self.file_names)):
                if self.mode == 'conversion':
                    conv.convert_image_to_webp(
                        file_path=file_path,
                        save_path=self.save_path + '/',
                        save_name=file_name,
                        lossless_option=self.config_options['conversion_loseless'],
                        image_quality_option=self.config_options['conversion_quality'],
                        exif_option=self.config_options['conversion_exif'],
                        icc_profile_option=self.config_options['conversion_icc'],
                        exact_option=self.config_options['conversion_transparent'],
                        watermark_text="",
                        conversion_option=True,
                        resize_option=self.config_options['resize_option'],
                        axis_option=self.config_options['resize_options'],
                        resize_value=self.config_options['resize_size']
                    )
                elif self.mode == 'exif':
                    conv.convert_exif_image(
                        file_path=file_path,
                        save_path=self.save_path + '/',
                        save_name=file_name,
                        file_format_option=self.config_options['exif_type'],
                        font_path=self.font_path,
                        bg_color=self.config_options['exif_bg_color'],
                        text_color=self.config_options['exif_text_color'],
                        ratio_option=self.config_options['exif_ratio'],
                        exif_padding_option=self.config_options['exif_padding_mode'],
                        save_exif_data_option=self.config_options['exif_save_exifdata'],
                        resize_option=self.config_options['resize_option'],
                        axis_option=self.config_options['resize_axis'],
                        alignment_option=self.config_options['exif_format_alignment'],
                        resize_value=self.config_options['resize_size'],
                        quality_option=self.config_options['exif_quality'],
                        caption_format=self.config_options['exif_format'],
                        easymode_option=self.config_options['exif_easymode_options'],
                        easymode_oneline=self.config_options['exif_easymode_oneline'],
                        auto_hide_nonedata=self.config_options['exif_auto_hide_nonedata']
                    )
                
                self.progress.emit(int((index + 1) / total_files * 100))
                
            self.finished_conversion.emit(self.save_path)
            
        except Exception as e:
            self.error.emit(str(e))
