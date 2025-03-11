import sys
import os
from pathlib import Path

def resource_path(relative_path):
    """ PyInstaller 번들 환경과 개발 환경 모두에서 리소스 경로 처리 """
    try:
        base_path = sys._MEIPASS  # 번들 실행 시 임시 폴더
    except AttributeError:
        # 개발 환경: 프로젝트 루트 기준 상대 경로
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../resources'))
    
    full_path = os.path.join(base_path, relative_path)
    
    # 경로 정규화 (상대 경로 ../ 제거)
    full_path = os.path.normpath(full_path)
    
    # 파일 존재 여부 확인 (옵셔널)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Missing critical resource: {full_path}")
    
    return full_path