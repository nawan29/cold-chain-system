基于 MQTT 的智能冷链物流监测与预警系统
本项目是一个基于物联网架构的实时数据监测系统。通过 Python 模拟 ESP32 硬件采集温湿度数据，利用 MQTT 协议进行传输，后端使用 FastAPI 接收数据并存入 MySQL 数据库，同时利用 Pandas 进行数据分析和异常识别，最后通过 Streamlit 实现实时监控与预警大屏。

技术栈
硬件模拟：Python / paho-mqtt

消息中间件：MQTT (EMQX 公共服务器)

后端服务：FastAPI / Python

数据库：MySQL

数据分析：Pandas

前端可视化：Streamlit

核心功能
设备端模拟：定时生成温湿度数据，发布到 MQTT 主题。

数据接收与存储：后端订阅 MQTT 主题，实时接收数据并写入 MySQL。

智能异常分析：利用 Pandas 筛选超标数据（温度 > 8℃ 或 < 2℃ 判定为异常）。

实时可视化：Streamlit 展示实时指标、趋势折线图、历史数据以及红色异常警报。

快速启动
安装依赖：pip install fastapi uvicorn paho-mqtt pymysql pandas streamlit requests

初始化数据库：在 MySQL 中创建数据库 cold_chain_db 和表 sensor_data。

修改配置：在 database.py 中填入你的 MySQL 密码。

启动虚拟硬件：python virtual_esp32.py

启动后端服务：python -m uvicorn main:app --reload --port 8000

启动前端大屏：streamlit run frontend.py

注意事项
运行本项目需要同时开启三个终端窗口，分别执行上述的第 4、5、6 步。确保 MySQL 服务已启动，并且 MQTT 服务器网络通畅。
