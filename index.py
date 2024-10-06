import subprocess
import random
import string
import time

# Hàm thực hiện lệnh adb thông qua cmd
def adb_command(command):
    full_command = f'adb {command}'
    process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error: {stderr.decode('utf-8')}")
    return stdout.decode('utf-8')

# Hàm click vào vị trí (x, y)
def adb_click(x, y):
    command = f"shell input tap {x} {y}"
    adb_command(command)

# Hàm nhập văn bản
def adb_input_text(text):
    command = f'shell input text "{text}"'
    adb_command(command)

# Hàm gửi event "Enter"
def adb_send_enter():
    command = "shell input keyevent 66"  # KeyEvent 66 là Enter
    adb_command(command)

# Tạo chuỗi ngẫu nhiên gồm 5 ký tự (chỉ bao gồm chữ cái và số)
def random_string(length=5):
    chars = string.ascii_letters + string.digits  # Chữ cái và số
    return ''.join(random.choice(chars) for _ in range(length))

# Main loop
def main_loop():
    while True:
        # Bước 1: Click vào điểm thứ nhất (x=676, y=675)
        adb_click(676, 675)

        # Bước 2: Tạo chuỗi ngẫu nhiên và nhập văn bản
        random_chars = random_string(5)
        input_text = f"Test Click{random_chars}"

        # Bước 3: Nhập văn bản vào thiết bị
        adb_input_text(input_text)

        # Bước 4: Gửi event Enter
        adb_send_enter()

        # Bước 5: Click vào điểm thứ hai (x=859, y=675)
        adb_click(859, 675)

        # Bước 6: Đợi 30 giây trước khi lặp lại
        time.sleep(30)

if __name__ == "__main__":
    main_loop()