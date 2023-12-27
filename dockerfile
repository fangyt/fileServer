# 使用阿里云的 CentOS 镜像
FROM centos:8

# 切换到阿里云的镜像源
RUN echo -e "[centos]\nname=CentOS Linux\nbaseurl=https://mirrors.aliyun.com/centos/\$releasever/os/\$basearch/\ngpgcheck=1\ngpgkey=https://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-Official\nenabled=1" > /etc/yum.repos.d/CentOS-Base.repo && \
    dnf makecache

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
