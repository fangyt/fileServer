# 第一阶段：构建应用程序
FROM ubuntu:20.04

# 安装基本工具和依赖项
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        wget \
        make \
        gcc \
        python3 \
        python3-pip \
        nginx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /App

# 复制并解压应用程序代码
ADD app.tar.gz .

## 安装应用程序依赖项
RUN pip3 install --no-cache-dir -r ./requirements.txt

# 复制 Nginx 配置文件
 COPY nginx.conf /etc/nginx/sites-available/default

# 暴露应用程序运行的端口
EXPOSE 5000

# 启动应用程序
CMD ["sh", "-c", "python3 ./app.py & nginx -g 'daemon off;'"]