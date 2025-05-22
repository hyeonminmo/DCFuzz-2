ARG FUZZER_PREFIX
FROM $FUZZER_PREFIX/windranger

RUN mkdir /d

COPY source/ /dcfuzz_bench

COPY target_line/ /dcfuzz_bench/target_line

#RUN cd /dcfuzz_bench/benchmark_project

COPY windranger/build_all.sh /

RUN /build_all.sh

