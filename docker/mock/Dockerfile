FROM ubuntu:latest

LABEL version="2.0"
LABEL Christian Sargusingh "https://github.com/cSDes1gn"

# Grab dependencies and generate locale
WORKDIR /app

# add package dependancy indices
COPY apt-packages.txt /app/apt-packages.txt
RUN apt update && \
    apt upgrade -y && \
    apt install -y git sudo locales && \
    locale-gen en_US.UTF-8 && \
    DEBIAN_FRONTEND=noninteractive TZ=America/New_York xargs -a apt-packages.txt apt install -y --no-install-recommends --fix-missing

COPY . .
# install hwi from source
RUN python3 -m pip install .

ENTRYPOINT [ "python3", "-m", "hwi" ]