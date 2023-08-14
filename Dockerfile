# 基础镜像
FROM python:3.10

# 设置工作目录
WORKDIR /app

# 复制文件到镜像中的 /app 目录下
COPY ./backend /app
COPY ./requirements.txt /app
#COPY ./entrypoint.sh /app

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

# 将容器的 8000 端口暴露出来
EXPOSE 8000

# 启动 Gunicorn 服务器
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]

#ENTRYPOINT ["sh","/app/entrypoint.sh"]
