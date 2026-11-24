import paho.mqtt.client as mqtt
import time
import random
import json

# MQTT 服务器配置（使用公共免费测试服务器）
BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "cold_chain/sensor/data" # 主题：冷链传感器数据

def on_connect(client, userdata, flags, rc):
    print(f"虚拟 ESP32 已连接 MQTT 服务器，返回码: {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.connect(BROKER, PORT, 60)
client.loop_start()

print("开始发送温湿度数据...")
try:
    while True:
        # 模拟生成温湿度数据（冷链标准通常是 2~8 度）
        # 我们故意让温度偶尔升到 10 度以上，用来测试预警功能
        temperature = round(random.uniform(2.0, 10.0), 1)
        humidity = round(random.uniform(40.0, 60.0), 1)
        
        payload = {
            "device_id": "ESP32-001",
            "temperature": temperature,
            "humidity": humidity
        }
        
        # 发送 JSON 格式的数据
        client.publish(TOPIC, json.dumps(payload))
        print(f"已发送: {payload}")
        
        time.sleep(3) # 每 3 秒发一次
except KeyboardInterrupt:
    print("停止发送")
    client.loop_stop()