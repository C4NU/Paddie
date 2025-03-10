# Copyright 2023 Hyo Jae Jeon (CANU) canu1832@gmail.com

########################################
import sys  # 시스템 모듈
########################################

def main():
    print(sys.version)
    import app_window
    print("App Window module Loaded")
    app = app_window.WebpApp()
    print("Webp App Module Loaded")
    app.show()
    app.exec()

if __name__ == "__main__":
    main()
