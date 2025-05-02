# Sử dụng Python 3.9 làm base image
FROM python:3.9-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Cài đặt các dependencies cần thiết
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release \
    jq \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt Google Cloud SDK
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && mkdir -p /usr/share/keyrings \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - \
    && apt-get update && apt-get install -y google-cloud-sdk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt trước để tận dụng Docker cache
COPY requirements.txt .

# Cài đặt Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy tất cả source code vào container
COPY . .

# Tạo các thư mục cần thiết
RUN mkdir -p data queries api/config config

# Đặt biến môi trường
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Cấp quyền thực thi cho script
RUN chmod +x run.sh

# Expose port cho FastAPI
EXPOSE ${PORT}

# Command để chạy ứng dụng
CMD ["python", "main.py", "--host", "0.0.0.0", "--port", "8000"]