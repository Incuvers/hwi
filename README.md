# IRIS Hardware Interface
[![ci](https://github.com/Incuvers/hwi/actions/workflows/ci.yml/badge.svg)](https://github.com/Incuvers/hwi/actions/workflows/ci.yml)
[![deploy](https://github.com/Incuvers/hwi/actions/workflows/image.yml/badge.svg)](https://github.com/Incuvers/hwi/actions/workflows/image.yml)
![img](/docs/img/Incuvers-black.png)

Updated: 2021-11

## Navigation
1. [Quickstart](#quickstart)
2. [Developer Team](#development-team)
3. [Licence](#license)

## Quickstart
This repository is built and controlled using the Makefile in the root in order to homogenize our dev environments. Run `make help` for more information on the available make targets. The source is intended to be built and developed on Ubuntu 20.04 or higher ARM64 systems.

Install `docker`, `docker-compose` and setup user permissions
```bash
sudo apt install docker.io docker-compose
sudo groupadd docker
sudo usermod -aG docker $USER
sudo reboot
```

### Authentication
Create a `.env` file from the sample env file
```bash
cp sample.env .env
```

### Docker Environment
Build the services for local development. Local source code is mounted to the `hwi` container for rapid development:
```bash
make dev
```

### Python Module
Or run the python module directly:
```bash
python3 -m hwi
```

## Development Team
David Sean (CTO) (david@incuvers.com)\
Christian Sargusingh (christian@incuvers.com)
