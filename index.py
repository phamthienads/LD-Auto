import subprocess
import random
import string
import time

def adb_command(command, device_serial):
    full_command = f'adb -s {device_serial} {command}'
    process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error on device {device_serial}: {stderr.decode('utf-8')}")
    return stdout.decode('utf-8')

def get_connected_devices():
    result = subprocess.run("adb devices", shell=True, capture_output=True, text=True)
    lines = result.stdout.splitlines()[1:]
    devices = [line.split()[0] for line in lines if "device" in line]
    return devices

def adb_click(x, y, device_serial):
    command = f"shell input tap {x} {y}"
    adb_command(command, device_serial)
    print(f"[{device_serial}] Clicked at ({x}, {y})")

def adb_past_text(device_serial):
    command = f'shell input keyevent 279'
    adb_command(command, device_serial)
    random_chars = random_string(5)
    command = f'shell input text "%s{random_chars}"'
    adb_command(command, device_serial)
    print(f"Pasted text to {device_serial}")

def adb_send_enter(device_serial):
    command = "shell input keyevent 66"
    adb_command(command, device_serial)
    print(f"[{device_serial}] Sent Enter key event")

def random_string(length=5):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def countdown(seconds):
    for remaining in range(seconds, 0, -1):
        print(f"Waiting: {remaining} seconds remaining", end='\r')
        time.sleep(1)
    print("\n")

def main_loop():
    devices = get_connected_devices()
    if not devices:
        print("No devices connected.")
        return
    
    while True:
        for device in devices:
            adb_click(676, 675, device)
            time.sleep(1)
            adb_past_text(device)
            time.sleep(1)
            adb_send_enter(device)
            time.sleep(1)
            adb_click(859, 675, device)
            time.sleep(1)
        countdown(30)

if __name__ == "__main__":
    main_loop()