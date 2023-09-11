# Copyright 2023 Hyo Jae Jeon (CANU) canu1832@gmail.com

########################################
import sys  # 시스템 모듈
import os
########################################

def main():
    import app_window
    app = app_window.WebpApp()
    app.show()
    app.exec()

    # t = test_module.test.TestClass()


if __name__ == "__main__":
    main()
