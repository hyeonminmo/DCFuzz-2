ARG PREFIX
FROM $PREFIX/base

WORKDIR /fuzzer

COPY fuzzer_base/windranger/windranger.tar.gz /fuzzer/

RUN tar -xzf windranger.tar.gz && \
    rm windranger.tar.gz && \
    mv windranger WindRanger

# Install LLVM-10
RUN wget https://github.com/llvm/llvm-project/releases/download/llvmorg-10.0.0/clang+llvm-10.0.0-x86_64-linux-gnu-ubuntu-18.04.tar.xz && \
    tar -xf clang+llvm-10.0.0-x86_64-linux-gnu-ubuntu-18.04.tar.xz && \
    rm clang+llvm-10.0.0-x86_64-linux-gnu-ubuntu-18.04.tar.xz && \
    mv clang+llvm-10.0.0-x86_64-linux-gnu-ubuntu-18.04 /fuzzer/WindRanger/clang+llvm

# Set environment variables instead of symbolic linking
ENV LLVM_PATH=/fuzzer/WindRanger/clang+llvm
ENV PATH=$LLVM_PATH/bin:$PATH
#ENV GOPATH=/root/go
#ENV PATH=$LLVM_PATH/bin:$GOPATH/bin:$PATH
ENV CC=$LLVM_PATH/bin/clang
ENV CXX=$LLVM_PATH/bin/clang++
ENV LLVM_COMPILER=clang
ENV WLLVM_CONFIGURE_ONLY=1


# Install wllvm
RUN pip3 install --upgrade pip==9.0.3 && \
    pip3 install wllvm

# Install gclang
#RUN mkdir -p $GOPATH && \
#    go install github.com/SRI-CSL/gllvm/cmd/gclang@v1.3.0 && \
#    go install github.com/SRI-CSL/gllvm/cmd/get-bc@v1.3.0 && \
#    go install github.com/SRI-CSL/gllvm/cmd/llvm-link-whole@v1.3.0
