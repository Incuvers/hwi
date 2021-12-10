FROM ubuntu:latest

LABEL version="2.0"
LABEL Christian Sargusingh "https://github.com/cSDes1gn"

WORKDIR /app

COPY docker/mock /app/mock/
RUN python3 -m pip install -r requirements.txt

ENTRYPOINT [ "python3", "-m", "hwi" ]