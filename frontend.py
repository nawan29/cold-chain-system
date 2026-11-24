import streamlit as st
import requests
import pandas as pd
import time

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="智能冷链监测", page_icon="❄️", layout="wide")
st.title("❄️ 智能冷链物流监测与预警系统")

# 侧边栏
with st.sidebar:
    st.header("系统控制")
    auto_refresh = st.checkbox("开启实时刷新 (每3秒)", value=True)
    if st.button("手动刷新数据"):
        st.rerun()

# 获取数据
def fetch_data():
    try:
        res = requests.get(f"{API_BASE}/api/data")
        return pd.DataFrame(res.json())
    except:
        return pd.DataFrame()

df = fetch_data()

if df.empty:
    st.warning("暂无数据，请确保虚拟 ESP32 和后端已启动。")
else:
    # 数据反转，让最新的在最前面
    df = df.sort_values(by="id", ascending=False)
    
    # 顶部指标
    col1, col2, col3 = st.columns(3)
    latest_temp = df.iloc[0]['temperature']
    latest_hum = df.iloc[0]['humidity']
    
    col1.metric("当前温度 (°C)", f"{latest_temp} °C", delta=f"{latest_temp - 4} °C (基准4度)")
    col2.metric("当前湿度 (%)", f"{latest_hum} %")
    col3.metric("系统状态", "异常" if latest_temp > 8 or latest_temp < 2 else "正常",
                delta_color="inverse" if latest_temp > 8 or latest_temp < 2 else "normal")

    # 绘制折线图
    st.subheader("📈 最近温湿度变化趋势")
    chart_data = df.set_index("record_time")[["temperature", "humidity"]]
    st.line_chart(chart_data)

    # 历史数据表格
    st.subheader("📋 历史监测数据")
    st.dataframe(df, use_container_width=True)

    # 异常预警（调用 Pandas 分析接口）
    st.subheader("🚨 异常预警记录")
    try:
        alerts = requests.get(f"{API_BASE}/api/alerts").json().get('alerts', [])
        if alerts:
            st.error(f"发现 {len(alerts)} 条温湿度异常记录！请立即检查冷链设备！")
            st.dataframe(pd.DataFrame(alerts), use_container_width=True)
        else:
            st.success("所有数据正常，未发现异常。")
    except:
        st.error("预警接口获取失败")

# 自动刷新逻辑
if auto_refresh:
    time.sleep(3)
    st.rerun()