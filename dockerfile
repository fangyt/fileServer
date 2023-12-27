# 使用阿里云的 CentOS 镜像
FROM centos:latest

# 安装基本工具和依赖项
RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/Centos-*
RUN sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/Centos-*
RUN wget -O /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-vault-8.5.2111.repo
RUN yum -y install epel-release && \
    yum -y update && \
    yum -y install \
        python38 \
        nginx \
    && dnf clean all

# 设置工作目录
ADD . /app
WORKDIR /app

# 复制应用程序的依赖项文件
COPY requirements.txt .

# 安装应用程序依赖项
RUN pip3.8 install --no-cache-dir -r requirements.txt

# 复制应用程序代码
COPY . .

# 复制 Nginx 配置文件
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露应用程序运行的端口
EXPOSE 5000

# 启动 Nginx 和应用程序
CMD ["nginx", "-g", "daemon off;"]
