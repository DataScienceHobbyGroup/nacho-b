# 1. Base image
FROM python:3.9-slim-buster

# 2. Copy files
WORKDIR /project
COPY . .

# 3. Set args and env vars
ARG GIT_HASH
# -dev is default if no arg specified
ENV GIT_HASH=${GIT_HASH:-dev} 
# . Install dependencies
RUN pip install -r /src/requirements.txt
