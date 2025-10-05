# 使用官方 uv + Python 3.13 + Alpine 镜像
FROM ghcr.io/astral-sh/uv:python3.13-alpine

# 工作目录
WORKDIR /opt/neoDTH

# 安装系统依赖（适合 Alpine）
RUN apk update && apk add --no-cache \
    gcc python3-dev musl-dev \
    bash nginx vim curl procps net-tools tzdata

# 设置时区
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone

# 拷贝依赖文件（uv 用法）
COPY pyproject.toml uv.lock ./
RUN uv sync

# 拷贝项目源代码
COPY . .

# 暴露端口（FastAPI）
EXPOSE 8000

# 启动命令：使用 uv run 调用 uv 环境下的 fastapi
CMD ["python", "main.py"]
