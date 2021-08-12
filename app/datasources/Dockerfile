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
wheel 

# Set working directory
WORKDIR /app/datasources

# Copy resource files
COPY /resources/* ./resources/

# Make the data folder
RUN mkdir data/

# create user
RUN useradd -m -r nacho && \
chown -R nacho .

# Install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy files
COPY *.py .

# set user
USER nacho

# Entry point
ENTRYPOINT python ticker_scraper.py