FROM ubuntu:bionic-20210512

# Install Python3.
RUN apt update -y && \
    apt install -y \
        python3 \
        python3-pip

# Upgrade pip.
# https://stackoverflow.com/questions/56357794/unable-to-install-grpcio-using-pip-install-grpcio
RUN pip3 install --upgrade pip && \
    python3 -m pip install --upgrade setuptools

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt

COPY uwu_links /app

CMD ["/app/server.py"]
