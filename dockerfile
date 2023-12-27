# Dockerfile

# 使用官方 Python 镜像
FROM python:3.8-slim

# 设置工作目录
WORKDIR /app

# 复制应用程序的依赖项文件
COPY requirements.txt .

# 安装依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 安装 Nginx
RUN yum check-update \
    && yum install -y nginx \
    && rm -rf /var/lib/apt/lists/*

# 复制 Nginx 配置文件
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 复制应用程序代码
COPY . .

# 暴露应用程序运行的端口
EXPOSE 5000

# 启动 Nginx 和应用程序
CMD ["nginx", "-g", "daemon off;"]
