FROM ubuntu:20.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# 安装依赖
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    git \
    zip \
    unzip \
    openjdk-8-jdk \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安装buildozer
RUN pip3 install buildozer

# 设置工作目录
WORKDIR /app

# 复制应用文件
COPY . .

# 设置权限
RUN chmod +x buildozer.spec

# 构建APK
RUN buildozer android debug

# 复制生成的APK到输出目录
RUN mkdir -p /output && cp bin/*.apk /output/
