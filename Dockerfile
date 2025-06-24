FROM fuzzer_base/aflgo as aflgo
FROM fuzzer_basse/windranger as windranger

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










