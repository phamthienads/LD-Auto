import subprocess
import random
import string
import time

# Hàm thực hiện lệnh adb cho một thiết bị cụ thể (theo serial)
def adb_command(command, device_serial):
    full_command = f'adb -s {device_serial} {command}'
    process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error on device {device_serial}: {stderr.decode('utf-8')}")
    return stdout.decode('utf-8')

# Lấy danh sách các thiết bị kết nối
def get_connected_devices():
    result = subprocess.run("adb devices", shell=True, capture_output=True, text=True)
    lines = result.stdout.splitlines()[1:]  # Bỏ qua dòng đầu tiên "List of devices attached"
    devices = [line.split()[0] for line in lines if "device" in line]
    return devices

# Hàm click vào vị trí (x, y) cho một thiết bị cụ thể
def adb_click(x, y, device_serial):
    command = f"shell input tap {x} {y}"
    adb_command(command, device_serial)
    print(f"[{device_serial}] Clicked at ({x}, {y})")

# Hàm nhập văn bản cho một thiết bị cụ thể
def adb_input_text(text, device_serial):
    command = f'shell input text "{text}"'
    adb_command(command, device_serial)
    print(f"[{device_serial}] Input text: {text}")

# Hàm gửi event "Enter" cho một thiết bị cụ thể
def adb_send_enter(device_serial):
    command = "shell input keyevent 66"  # KeyEvent 66 là Enter
    adb_command(command, device_serial)
    print(f"[{device_serial}] Sent Enter key event")

# Tạo chuỗi ngẫu nhiên gồm 5 ký tự (chỉ bao gồm chữ cái và số)
def random_string(length=5):
    chars = string.ascii_letters + string.digits  # Chữ cái và số
    return ''.join(random.choice(chars) for _ in range(length))

# Hiển thị đếm ngược trong quá trình chờ
def countdown(seconds):
    for remaining in range(seconds, 0, -1):
        print(f"Waiting: {remaining} seconds remaining", end='\r')
        time.sleep(1)
    print("\n")

# Main loop điều khiển tất cả các thiết bị
def main_loop():
    devices = get_connected_devices()
    if not devices:
        print("No devices connected.")
        return
    
    while True:
        for device in devices:
            # Bước 1: Click vào điểm thứ nhất (x=676, y=675) cho từng thiết bị
            adb_click(676, 675, device)

            # Bước 2: Tạo chuỗi ngẫu nhiên và nhập văn bản cho từng thiết bị
            random_chars = random_string(5)
            input_text = f"Test Click{random_chars}"
            adb_input_text(input_text, device)

            # Bước 3: Gửi event Enter cho từng thiết bị
            adb_send_enter(device)

            # Bước 4: Click vào điểm thứ hai (x=859, y=675) cho từng thiết bị
            adb_click(859, 675, device)

        # Bước 5: Đếm ngược trong 30 giây trước khi lặp lại
        countdown(30)

if __name__ == "__main__":
    main_loop()