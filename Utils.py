import requests

class counter:
    def __init__(self):
        self.i = 0

    def plus(self, steps=1):
        self.i += steps

    def clear(self):
        self.i = 0
    
    def show(self):
        return self.i
    


class ServerChan:
    def __init__(self, send_key: str):
        self.api_url = f"https://sctapi.ftqq.com/{send_key}.send"

    def send(self, title: str, content: str):
        data = {
            "title": title,
            "desp": content
        }
        try:
            resp = requests.post(self.api_url, data=data, timeout=5)
            resp.raise_for_status()
            result = resp.json()
            if result.get("code") == 0:
                print("消息发送成功✅")
            else:
                print(f"发送失败❌: {result}")
        except Exception as e:
            print(f"发送失败，错误信息: {e}")

# 示例用法
if __name__ == "__main__":
    send_key = "SCT291449TTW7hQ0QFBL9ibAQ9NVFSIgJE"  # 替换成你的 SendKey
    notifier = ServerChan(send_key)
    notifier.send("服务器状态", "✅ 服务已启动，监听端口 8080")