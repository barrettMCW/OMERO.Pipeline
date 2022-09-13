FROM python:3.7

# update system
RUN apt update && apt upgrade -y && apt install -y python3-pip

# Keeps Python from generating .pyc files in the container 
ENV PYTHONDONTWRITEBYTECODE=1 
 
# Turns off buffering for easier container logging 
ENV PYTHONUNBUFFERED=1 

RUN useradd -s /bin/bash -m vscode \
 && groupadd docker \
 && usermod -aG docker vscode
USER vscode

RUN python3.7 -m pip install --upgrade pip

COPY requirements.txt /tmp

RUN python3.7 -m pip install -r /tmp/requirements.txt