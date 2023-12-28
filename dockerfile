# Dockerfile
FROM python:3.8-slim

WORKDIR /app

# 安装 Flask 和相关依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用程序代码
COPY app /app

# 暴露应用程序运行的端口
EXPOSE 5000

# 启动应用程序
CMD ["python", "app.py"]
