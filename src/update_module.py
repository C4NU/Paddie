import os
import sys
import platform
import json
import requests
import zipfile
import subprocess
import shutil
import tempfile
from PyQt6.QtCore import QObject, pyqtSignal, QThread

class UpdateWorker(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, download_url, save_path):
        super().__init__()
        self.download_url = download_url
        self.save_path = save_path

    def run(self):
        try:
            response = requests.get(self.download_url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            if total_size == 0:
                self.finished_signal.emit(False, "Invalid file size")
                return

            downloaded = 0
            with open(self.save_path, 'wb') as f:
                for data in response.iter_content(chunk_size=4096):
                    downloaded += len(data)
                    f.write(data)
                    progress = int((downloaded / total_size) * 100)
                    self.progress_signal.emit(progress)
            
            self.finished_signal.emit(True, self.save_path)
        except Exception as e:
            self.finished_signal.emit(False, str(e))

class UpdateManager(QObject):
    GITHUB_API_URL = "https://api.github.com/repos/C4NU/Paddie/releases/latest" 

    def __init__(self, current_version):
        super().__init__()
        self.current_version = current_version
        self.update_worker = None

    def check_for_update(self):
        try:
            response = requests.get(self.GITHUB_API_URL, timeout=5)
            if response.status_code == 200:
                data = response.json()
                latest_version = data['tag_name'].replace('v', '')
                
                if self._compare_versions(latest_version, self.current_version) > 0:
                    assets = data.get('assets', [])
                    download_url = self._get_platform_asset(assets)
                    return True, latest_version, download_url, data.get('body', '')
            return False, self.current_version, None, ""
        except Exception as e:
            print(f"Update check failed: {e}")
            return False, self.current_version, None, ""

    def _compare_versions(self, v1, v2):
        v1_parts = [int(p) for p in v1.split('.')]
        v2_parts = [int(p) for p in v2.split('.')]
        for i in range(max(len(v1_parts), len(v2_parts))):
            p1 = v1_parts[i] if i < len(v1_parts) else 0
            p2 = v2_parts[i] if i < len(v2_parts) else 0
            if p1 > p2: return 1
            if p1 < p2: return -1
        return 0

    def _get_platform_asset(self, assets):
        system = platform.system()
        for asset in assets:
            name = asset['name'].lower()
            if system == "Windows" and "windows" in name and name.endswith(".zip"):
                return asset['browser_download_url']
            if system == "Darwin" and "macos" in name and name.endswith(".zip"):
                return asset['browser_download_url']
            if system == "Linux" and "linux" in name and name.endswith(".zip"):
                return asset['browser_download_url']
        return None

    def start_download(self, download_url, progress_callback, finished_callback):
        temp_dir = tempfile.gettempdir()
        save_path = os.path.join(temp_dir, "paddie_update.zip")
        
        self.update_worker = UpdateWorker(download_url, save_path)
        self.update_worker.progress_signal.connect(progress_callback)
        self.update_worker.finished_signal.connect(finished_callback)
        self.update_worker.start()

    def sync_program_data(self, latest_version):
        """서버에서 받은 최신 버전 정보를 program_data.json에 기록합니다."""
        try:
            # 실제 파일 시스템의 경로를 찾기 위해 resource_path 활용 (frozen 모드 고려)
            if getattr(sys, 'frozen', False):
                # frozen 모드일 때 sys._MEIPASS는 임시 폴더이므로, 실제 실행 파일 위치 기준 경로 계산
                if platform.system() == "Darwin":
                    # Paddie.app/Contents/MacOS/Paddie -> Paddie.app/Contents/Resources/resources/program_data.json
                    base_dir = os.path.abspath(os.path.join(os.path.dirname(sys.executable), "..", "Resources"))
                else:
                    # Windows/Linux: executable_dir/_internal/resources/program_data.json (onedir 기준)
                    base_dir = os.path.dirname(sys.executable)
                
                path = os.path.join(base_dir, "resources", "program_data.json")
            else:
                # 개발 모드
                from resource_path import resource_path
                path = resource_path("resources/program_data.json")

            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                data['version'] = latest_version
                
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                print(f"program_data.json updated to version {latest_version}")
                return True
        except Exception as e:
            print(f"Failed to sync program_data: {e}")
        return False

    def apply_update(self, zip_path):
        """
        압축을 풀고 업데이터를 실행합니다.
        """
        temp_extract_dir = os.path.join(tempfile.gettempdir(), "paddie_temp")
        if os.path.exists(temp_extract_dir):
            shutil.rmtree(temp_extract_dir)
        os.makedirs(temp_extract_dir)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_extract_dir)

        # 업데이터 스크립트 실행 경로 설정
        updater_script = self._create_updater_script(temp_extract_dir)
        
        # 메인 프로세스 종료 및 업데이터 실행
        if platform.system() == "Windows":
            subprocess.Popen(["python", updater_script], shell=True)
        else:
            subprocess.Popen(["python3", updater_script])
        
        sys.exit(0)

    def _create_updater_script(self, extract_dir):
        # 실행 중인 앱의 경로 및 플랫폼 확인
        is_frozen = getattr(sys, 'frozen', False)
        system = platform.system()
        
        if is_frozen:
            if system == "Darwin":
                # sys.executable: .../Paddie.app/Contents/MacOS/Paddie
                # app_bundle_path: .../Paddie.app
                app_bundle_path = os.path.abspath(os.path.join(os.path.dirname(sys.executable), "../.."))
                # parent_path: .../ (where Paddie.app is located)
                parent_path = os.path.dirname(app_bundle_path)
                
                app_path = parent_path
                executable = app_bundle_path
            else:
                app_path = os.path.dirname(sys.executable)
                executable = sys.executable
        else:
            app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            executable = sys.executable if system == "Windows" else "python3"

        updater_content = f"""
import os
import shutil
import time
import subprocess
import sys
import platform

# 메인 프로세스가 종료될 때까지 충분히 대기
time.sleep(3)

source = r"{extract_dir}"
target = r"{app_path}"
system = "{system}"

try:
    # macOS의 경우 .app 번들 자체를 교체해야 할 수도 있음
    # 다운로드된 압축 파일 구조에 따라 다름 (Paddie.app이 들어있는지, 내용물만 있는지)
    
    for item in os.listdir(source):
        s = os.path.join(source, item)
        d = os.path.join(target, item)
        
        if os.path.exists(d):
            if os.path.isdir(d):
                shutil.rmtree(d)
            else:
                os.remove(d)
        
        if os.path.isdir(s):
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)
    
    # 앱 재실행
    if system == "Darwin":
        subprocess.Popen(["open", "{executable}"])
    elif system == "Windows":
        subprocess.Popen([r"{executable}"])
    else:
        subprocess.Popen(["{executable}"])
        
except Exception as e:
    with open(os.path.join(os.path.expanduser("~"), "paddie_update_error.log"), "w", encoding='utf-8') as f:
        f.write(str(e))
finally:
    # 임시 디렉토리 삭제 시도 (선택 사항)
    # shutil.rmtree(source)
    pass
"""
        updater_path = os.path.join(tempfile.gettempdir(), "paddie_updater.py")
        with open(updater_path, "w", encoding="utf-8") as f:
            f.write(updater_content)
        return updater_path
