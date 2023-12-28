# 第一阶段：构建应用程序
FROM ubuntu:20.04
# 打印当前工作目录路径
RUN pwd

# 安装基本工具和依赖项
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        wget \
        make \
        gcc \
        nginx \
        python3.8 \
        python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制应用程序的依赖项文件
COPY requirements.txt .

# 安装应用程序依赖项
RUN pip3 install --no-cache-dir -r requirements.txt

# 打印当前工作目录路径
RUN pwd

# 复制应用程序代码
COPY app /app/

# # 复制 Nginx 配置文件
# COPY nginx.conf /etc/nginx/sites-available/default

# 暴露应用程序运行的端口
EXPOSE 5000

# 启动 Nginx 和应用程序
# CMD service nginx start && python3 app/app.py
# CMD python3 -u ${pwd}/app/app.py

