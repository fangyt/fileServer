# 安装 Python 相关工具和依赖项
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 安装应用程序依赖项
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
