# 第一阶段：构建应用程序
FROM centos:8

# 更新系统并安装 Python 3
RUN yum -y update && yum -y install \
    python38 \
    && yum clean all

# 设置工作目录
WORKDIR /app

# 复制应用程序的依赖项文件
COPY requirements.txt .

# 安装应用程序依赖项
RUN pip3.8 install --no-cache-dir -r requirements.txt

# 复制应用程序代码
COPY . .

# 安装基础工具和依赖项
RUN yum -y update && yum -y install \
    nginx \
    && yum clean all

# 复制 Nginx 配置文件
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露应用程序运行的端口
EXPOSE 5000

# 启动 Nginx 和应用程序
CMD ["nginx", "-g", "daemon off;"]
