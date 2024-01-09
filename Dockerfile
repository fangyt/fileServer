# 第一阶段：构建应用程序
FROM ubuntu:20.04


# 安装基本工具和依赖项
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        wget \
        make \
        gcc \
        nginx \
        python3 \
        python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR ./

# 复制应用程序代码
ADD app.tar.gz /.

RUN ping -c 4 baidu.com

## 安装应用程序依赖项
#RUN pip3 install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r ./requirements.txt
#
## 复制 Nginx 配置文件
#COPY nginx.conf /etc/nginx/sites-available/default
#
## 暴露应用程序运行的端口
#EXPOSE 8089
#
##启动 Nginx 和应用程序
#CMD ["bash", "-c", "service nginx start && python3 ./app.py"]

