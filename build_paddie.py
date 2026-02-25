import json
import re
import os
import shutil
import subprocess

def update_build_info():
    # 1. 버전 정보 읽기
    program_data_path = 'resources/program_data.json'
    if not os.path.exists(program_data_path):
        print(f"Error: {program_data_path} not found.")
        return
        
    with open(program_data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        version = data.get('version', '1.0.0')
    
    print(f"Current version detected: {version}")

    # 2. Spec 파일 읽기 및 수정
    spec_path = 'Paddie.spec'
    if not os.path.exists(spec_path):
        print(f"Error: {spec_path} not found.")
        return

    with open(spec_path, 'r', encoding='utf-8') as f:
        spec_content = f.read()

    # bundle_identifier 업데이트 (macOS 표준에 가깝게 com.canu. 추가)
    new_bundle_id = 'com.canu.paddie_legacy'
    spec_content = re.sub(r"bundle_identifier\s*=\s*['\"].*?['\"]", f"bundle_identifier='{new_bundle_id}'", spec_content)
    
    # macOS에서 런타임 오류(Bootloader did not set sys._pyinstaller_pyz!)를 유발할 수 있는 UPX 비활성화
    spec_content = re.sub(r"upx\s*=\s*True", "upx=False", spec_content)
    
    with open(spec_path, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print(f"Updated {spec_path} with bundle_identifier='{new_bundle_id}' and upx=False")

    # 3. 기존 빌드 폴더 정리
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            print(f"Cleaning {folder} folder...")
            shutil.rmtree(folder)

    # 4. 빌드 실행
    print("Starting PyInstaller build...")
    try:
        # --clean 옵션을 추가하여 잔여 파일로 인한 오류 방지
        subprocess.run(['pyinstaller', '--noconfirm', '--clean', spec_path], check=True)
        print("Build completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
    except FileNotFoundError:
        print("Error: pyinstaller not found. Please install it using 'pip install pyinstaller'.")

if __name__ == "__main__":
    update_build_info()
