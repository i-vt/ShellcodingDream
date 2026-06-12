FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    gcc \
    g++ \
    gdb \
    make \
    mingw-w64 \
    nasm \
    git \
    curl \
    wget \
    vim \
    nano \
    netcat \
    metasploit-framework \
    ropper \
    radare2 \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir \
    pycryptodome==3.18.0 \
    requests==2.31.0 \
    colorama==0.4.6 \
    click==8.1.7 \
    tabulate==0.9.0 \
    pwntools==4.10.1 \
    scikit-learn==1.3.0 \
    numpy==1.24.0 \
    scipy==1.11.0 \
    capstone==5.0.0 \
    keystone-engine==0.9.2 \
    networkx==3.1

WORKDIR /shellcoding

COPY . /shellcoding/

RUN chmod +x /shellcoding/scripts/*.sh && \
    mkdir -p /output /shellcoding/.cache

WORKDIR /output

ENTRYPOINT ["/shellcoding/scripts/entrypoint.sh"]
CMD ["--help"]
