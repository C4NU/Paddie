import json
import re
import os
import subprocess

def update_build_info():
    # 1. 버전 정보 읽기
    program_data_path = 'resources/program_data.json'
    with open(program_data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        version = data.get('version', '1.0.0')
    
    print(f"Current version detected: {version}")

    # 2. Spec 파일 읽기 및 수정
    spec_path = 'Paddie.spec'
    with open(spec_path, 'r', encoding='utf-8') as f:
        spec_content = f.read()

    # bundle_identifier 업데이트
    # 사용자의 요청에 따라 'paddie_legacy' 형태로 셋업
    new_bundle_id = 'paddie_legacy'
    spec_content = re.sub(r"bundle_identifier\s*=\s*['\"].*?['\"]", f"bundle_identifier='{new_bundle_id}'", spec_content)
    
    # 버전 정보는 Spec 파일에 직접 필드가 없으므로, 필요하다면 주석이나 파일명 등에 반영 가능
    # 여기서는 Bundle ID 업데이트를 중점적으로 처리
    
    with open(spec_path, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print(f"Updated {spec_path} with bundle_identifier='{new_bundle_id}'")

    # 3. 빌드 실행
    print("Starting PyInstaller build...")
    try:
        subprocess.run(['pyinstaller', '--noconfirm', spec_path], check=True)
        print("Build completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
    except FileNotFoundError:
        print("Error: pyinstaller not found. Please install it using 'pip install pyinstaller'.")

if __name__ == "__main__":
    update_build_info()
