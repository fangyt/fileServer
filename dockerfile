
# 安装基础工具和依赖项
FROM centos:8

# 替换默认的 CentOS 镜像源为阿里云
RUN sed -i 's|^mirrorlist=|#mirrorlist=|g' /etc/yum.repos.d/CentOS-Base.repo && \
    sed -i 's|^#baseurl=http://mirror.centos.org|baseurl=http://mirrors.aliyun.com|g' /etc/yum.repos.d/CentOS-Base.repo && \
    yum -y update && \
    yum -y install nginx && \
    yum clean all


# 安装 Python 3.8
RUN wget https://www.python.org/ftp/python/3.8.12/Python-3.8.12.tgz \
    && tar xzf Python-3.8.12.tgz \
    && cd Python-3.8.12 \
    && ./configure --enable-optimizations \
    && make altinstall

# 设置工作目录
WORKDIR /app

# 复制应用程序的依赖项文件
COPY requirements.txt .

# 安装应用程序依赖项
RUN pip3.8 install --no-cache-dir -r requirements.txt

# 复制应用程序代码
COPY . .


# 第二阶段：构建最终镜像
FROM centos:latest

# 安装基础工具和依赖项
RUN yum -y update && yum -y install \
    nginx \
    && yum clean all

# 从第一阶段复制构建的应用程序
COPY --from=builder /app /app

# 复制 Nginx 配置文件
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露应用程序运行的端口
EXPOSE 5000

# 启动 Nginx 和应用程序
CMD ["nginx", "-g", "daemon off;"]
