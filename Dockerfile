# ============================================================
# Ombre Brain Docker Build (Dual Service)
# Docker 构建文件（双服务模式）
#
# Build: docker build -t ombre-brain .
# Run:   docker run -e OMBRE_API_KEY=your-key -p 8000:8000 -p 8010:8010 ombre-brain
# ============================================================

FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (leverage Docker cache)
# 先装依赖（利用 Docker 缓存）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files / 复制项目文件
COPY *.py .
COPY resources ./resources
COPY scripts ./scripts
COPY dashboard.html .
COPY dashboard_assets ./dashboard_assets
COPY config.example.yaml ./config.yaml
COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x scripts/*.sh entrypoint.sh

# Persistent mount points
# 持久化挂载点
VOLUME ["/app/buckets", "/app/state"]

# Default to streamable-http for container (remote access)
# 容器场景默认用 streamable-http
ENV OMBRE_TRANSPORT=streamable-http
ENV OMBRE_BUCKETS_DIR=/app/buckets
ENV OMBRE_STATE_DIR=/app/state

# Brain on 8000, Gateway on 8010
EXPOSE 8000
EXPOSE 8010

CMD ["bash", "/app/entrypoint.sh"]
