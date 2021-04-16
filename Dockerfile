# 1. Base image
FROM python:3.9-slim-buster

# 2. Copy files
COPY /src /src
COPY /data_temp /data_temp

# 3. Install dependencies
RUN pip install -r /src/requirements.txt
