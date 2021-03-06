# Base image
FROM python:3.9-slim-buster

# Pin library version
ENV TINI_VERSION="v0.19.0"

# Add tini to  handle zombie processes and signals
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

# Update pip, setuptools and wheel
RUN pip install -U \
pip \
setuptools \
wheel \
pylint

# Set working directory
WORKDIR /project

# create user
RUN useradd -m -r nacho && \
chown nacho /project

# Install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy files
COPY . .

# Lint files
RUN pylint **/*.py

# set user
USER nacho

# Set args and env vars
ARG GIT_HASH
# -dev is default if no arg specified
ENV GIT_HASH=${GIT_HASH:-dev} 

# Entry point
ENTRYPOINT ["/tini", "--"]