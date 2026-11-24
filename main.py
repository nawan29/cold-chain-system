from fastapi import FastAPI
import paho.mqtt.client as mqtt
import json
from database import get_db_connection
import threading

app = FastAPI(title="冷链物流监测系统")

# --- 1. MQTT 接收逻辑 ---
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        device_id = data['device_id']
        temp = data['temperature']
        hum = data['humidity']
        
        print(f"收到数据: 设备={device_id}, 温度={temp}, 湿度={hum}")
        
        # 存入 MySQL
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "INSERT INTO sensor_data (device_id, temperature, humidity) VALUES (%s, %s, %s)"
            cursor.execute(sql, (device_id, temp, hum))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"数据保存失败: {e}")

# 启动 MQTT 客户端（在后台线程运行）
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect("broker.emqx.io", 1883, 60)
mqtt_client.subscribe("cold_chain/sensor/data")
mqtt_client.loop_start()

# --- 2. FastAPI 接口 ---
@app.get("/api/data")
def get_data():
    """获取最近 50 条数据（供前端展示）"""
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT 50")
        result = cursor.fetchall()
    conn.close()
    return result

@app.get("/api/alerts")
def get_alerts():
    """利用 Pandas 进行异常数据分析（筛选温度 > 8 度或 < 2 度的记录）"""
    import pandas as pd
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM sensor_data")
        data = cursor.fetchall()
    conn.close()
    
    df = pd.DataFrame(data)
    if df.empty:
        return {"alerts": [], "message": "暂无数据"}
    
    # Pandas 数据分析：找出异常数据
    anomalies = df[(df['temperature'] > 8.0) | (df['temperature'] < 2.0)]
    
    # 转回字典格式返回
    return {"alerts": anomalies.to_dict(orient='records')}