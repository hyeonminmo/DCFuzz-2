FROM fuzzer_base/aflgo as aflgo
FROM fuzzer_base/windranger as windranger

FROM dcfuzz_bench/aflgo as bench_aflgo
FROM dcfuzz_bench/windranger as bench_windranger

FROM ubuntu:20.04

ARG USER
ARG UID
ARG GID

SHELL ["/bin/bash", "-c"]


ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONIOENCODING=utf8 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8


# Install proper tools

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential cmake git curl wget unzip \
    autoconf automake libtool bison flex \
    zlib1g-dev libssl-dev python3 python3-pip \
    llvm clang clang-format clang-tidy \
    ninja-build pkg-config lcov python3-setuptools \
    python3-dev libglib2.0-dev libxml2-dev \
    libncurses5-dev libsqlite3-dev \
    tzdata sudo vim tmux htop zsh


# Copy fuzzer image

COPY --chown=$UID:$GID --from=aflgo /fuzzer /fuzzer
COPY --chown=$UID:$GID --from=windranger /fuzzer /fuzzer


# Copy program with each fuzzer image 

COPY --chown=$UID:$GID --from=bench_aflgo /benchmark/bin /benchmark/bin
COPY --chown=$UID:$GID --from=bench_windranger /benchmark/bin /benchmark/bin



USER root


# install newer python3 
RUN apt install -y --no-install-recommends make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev tk-dev ca-certificates


WORKDIR /root



