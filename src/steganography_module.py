import numpy as np
import cv2

def encode_message(image_path, message):
    # 이미지 읽기
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("이미지를 읽을 수 없습니다.")
    
    # 이미지 분해
    rows, cols = image.shape[:2]
    max_blocks = (rows // 8) * (cols // 8)
    max_bits_per_block = 64  # 예상되는 각 블록당 숨げる 비트 수
    
    # 최대 메시지 길이 계산
    max_message_length = max_blocks * max_bits_per_block
    if len(message) > max_message_length:
        raise ValueError(f"메시지가 너무 깁니다. 최대 {max_message_length}개의 문자를 입력하십시오.")
    
    # 메시지를 64비트로 나누기 위한 준비
    binary = message_to_binary(message)
    binary += '0' * (max_bits_per_block - (len(binary) % max_bits_per_block))
    
    # 이미지 분할 및 DCT 변환
    encoded_image = image.copy()
    block_index = 0
    
    for i in range(0, rows, 8):
        for j in range(0, cols, 8):
            block = image[i:i+8, j:j+8]
            # DCT 변환 수행
            dct_coefficients = cv2.dct(block)
            
            # 메시지 비트 삽입
            if block_index < len(binary) // max_bits_per_block:
                start = 0 + (block_index * max_bits_per_block)
                end = start + max_bits_per_block
                for k in range(8):
                    for l in range(8):
                        dct_coefficients[k][l] = int(binary[start:end]) % 256
            block_index += 1
            
            # 역 DCT를 통해 수정된 블록 복원
            decoded_block = cv2.idct(dct_coefficients)
            
            # 수정된 블록을 이미지에 다시 삽입
            encoded_image[i:i+8, j:j+8] = decoded_block
    
    return encoded_image

def decode_message(encoded_image_path):
    # 인코딩된 이미지 읽기
    encoded_image = cv2.imread(encoded_image_path)
    if encoded_image is None:
        raise ValueError("인코딩된 이미지를 읽을 수 없습니다.")
    
    rows, cols = encoded_image.shape[:2]
    message_bits = []
    
    for i in range(0, rows, 8):
        for j in range(0, cols, 8):
            block = encoded_image[i:i+8, j:j+8]
            # DCT 변환 수행
            dct_coefficients = cv2.dct(block)
            
            # 메시지 비트 추출
            for k in range(8):
                for l in range(8):
                    bit = dct_coefficients[k][l] % 2
                    message_bits.append(str(bit))
    
    # 비트를 문자열로 변환 및 복호화
    binary_string = ''.join(message_bits)
    decoded_message = binary_to_message(binary_string)
    
    return decoded_message

# 보조 함수 정의
def message_to_binary(message):
    binary_list = []
    for char in message:
        binary = bin(ord(char))[2:].zfill(8)
        binary_list.append(binary)
    return ''.join(binary_list)

def binary_to_message(binary_string):
    # 8 bits per character
    n = int(len(binary_string) / 8)
    message = []
    for i in range(n):
        byte = binary_string[i*8 : (i+1)*8]
        char = chr(int(byte, 2))
        message.append(char)
    return ''.join(message)

# 테스트
image_path = "resources/test.jpg"
message = "Hello, World!"
encoded_image = encode_message(image_path, message)
cv2.imwrite("resources/encoded_test.jpg", encoded_image)
decoded_message = decode_message("resources/encoded_test.jpg")
print(decoded_message)
