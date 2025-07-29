import os
import subprocess
import socket
import time

# Step 1: 检查设备上是否已有 minitouch 文件
def check_minitouch_exists():
    # 运行 shell 命令检查 minitouch 是否存在
    result = subprocess.run(
        "adb shell [ -f /data/local/tmp/minitouch ] && echo 'Found' || echo 'Not found'", 
        shell=True, capture_output=True, text=True)
    
    return "Found" in result.stdout

# Step 2: 启动 adb 并推送 minitouch
def setup_minitouch():
    subprocess.run(f"adb connect localhost:16384", shell=True)
    # 检查 minitouch 是否已存在
    if check_minitouch_exists():
        print("minitouch already exists on the device.")
    else:
        print("minitouch not found. Uploading minitouch binary to the device...")
        # 获取设备的 ABI 类型
        ABI = subprocess.check_output(
            "adb shell getprop ro.product.cpu.abi", shell=True).decode().strip()
        
        print(f"Device ABI: {ABI}")
        
        # 推送 minitouch 二进制文件到设备
        subprocess.run(f"adb push libs/{ABI}/minitouch /data/local/tmp/", shell=True)
        
        # 赋予可执行权限
        subprocess.run("adb shell chmod +x /data/local/tmp/minitouch", shell=True)
    
    # 启动 minitouch
    print("Starting minitouch...")
    subprocess.Popen("adb shell /data/local/tmp/minitouch", shell=True)
    time.sleep(2)  # 等待 minitouch 启动

# Step 3: 连接到 minitouch
def connect_to_minitouch():
    # 获取设备的 adb 端口转发
    subprocess.run("adb forward tcp:1111 localabstract:minitouch", shell=True)

    # 连接到 minitouch
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 1111))
    return sock

# Step 4: 发送触摸命令
def send_touch(sock, x, y, pressure=50):
    # minitouch 协议格式
    command = f'd 0 {x} {y} {pressure}\nc\n'  # d: down, c: commit
    sock.send(command.encode())

    # 延迟一段时间模拟按下
    time.sleep(0.1)
    
    # 发送抬起命令
    sock.send(b'u 0\nc\n')  # u: up, c: commit

# Step 5: 模拟点击事件
def simulate_tap(x, y):
    sock = connect_to_minitouch()
    
    print(f"Simulating tap at ({x}, {y})")
    
    # 发送触摸命令
    send_touch(sock, x, y)

    # 关闭 socket
    sock.close()

if __name__ == '__main__':
    setup_minitouch()
    
    # 模拟点击屏幕中间 (假设屏幕分辨率为 1080x1920)
    simulate_tap(270, 810)