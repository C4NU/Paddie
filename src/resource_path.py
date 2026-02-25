import sys
import os
from pathlib import Path

import sys
import os
from pathlib import Path

def resource_path(relative_path: str, check_exists: bool = True) -> str:
    """
    Cross-platform 리소스 경로 생성기 (PyInstaller 빌드/개발 모드 자동 인식)
    
    Parameters:
        relative_path (str): 프로젝트 루트 기준 상대 경로 (e.g. 'resources/ui/resizeoption.ui')
        check_exists (bool): 파일 존재 여부를 확인할지 여부 (기본값 True)
        
    Returns:
        str: 실제 리소스 절대 경로
        
    Raises:
        FileNotFoundError: check_exists가 True인데 리소스가 존재하지 않을 때
    """
    # PyInstaller 번들 모드 감지
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = Path(sys._MEIPASS)
    else:
        # 개발 모드: 현재 파일 기준 2단계 상위 디렉토리를 프로젝트 루트로 가정
        base_path = Path(__file__).resolve().parent.parent

    # 경로 조합 및 정규화
    full_path = (base_path / relative_path).resolve()

    # 존재 여부 검증 (모든 OS에서 대소문자 구분)
    if check_exists and not full_path.exists():
        error_msg = (
            f"[리소스 누락] '{relative_path}'를 찾을 수 없습니다.\n"
            f"검색 위치: {'번들' if hasattr(sys, '_MEIPASS') else '개발'} 모드\n"
            f"기준 경로: {base_path}\n"
            f"시스템 경로: {full_path}"
        )
        raise FileNotFoundError(error_msg)

    return os.fspath(full_path)  # 모든 OS에서 호환되는 문자열 변환

'''
def resource_path(relative_path):
    """번들/개발 환경에 맞는 절대 경로 생성"""
    try:
        base_path = sys._MEIPASS  # 번들 실행 시 임시 폴더
    except AttributeError:
        # 개발 환경: 프로젝트 루트 기준
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    full_path = os.path.join(base_path, relative_path)
    
    # ../ 문제 해결 및 경로 정규화
    normalized_path = os.path.normpath(full_path)
    
    if not os.path.exists(normalized_path):
        raise FileNotFoundError(f"리소스 누락: {normalized_path}")
    
    return normalized_path
'''
'''
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
    
    return full_path'
'''