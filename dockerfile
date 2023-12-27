# 第一阶段：构建应用程序
FROM centos:8

# 安装基本工具和依赖项
RUN dnf -y install epel-release && \
    dnf -y update && \
    dnf -y install \
        python38 \
        nginx \
    && dnf clean all

# 设置工作目录
WORKDIR /app

# 复制应用程序的依赖项文件
COPY requirements.txt .

# 安装应用程序依赖项
RUN pip3.8 install --no-cache-dir -r requirements.txt

# 复制应用程序代码
COPY . .

# 清理缓存
RUN dnf clean all

# 复制 Nginx 配置文件
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露应用程序运行的端口
EXPOSE 5000

# 启动 Nginx 和应用程序
CMD ["nginx", "-g", "daemon off;"]
