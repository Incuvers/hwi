FROM ubuntu:latest

LABEL version="2.0"
LABEL Christian Sargusingh "https://github.com/cSDes1gn"

WORKDIR /app
RUN apt update && \
    apt upgrade -y && \
    apt install -y git sudo locales python3 python3-pip && \
    locale-gen en_US.UTF-8
COPY docker/mock /app/mock/
RUN python3 -m pip install -r requirements.txt

ENTRYPOINT [ "python3", "-m", "hwi" ]