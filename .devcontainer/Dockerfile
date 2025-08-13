# syntax=docker/dockerfile:1
# enable here documents.
# RUN cat <<EOF >> /home/vscode/.bashrc
#
# EOF

# Stage 1
FROM ubuntu:latest as builder
# suppress clear apt cache
RUN rm /etc/apt/apt.conf.d/docker-clean

ARG ARG_TARGET=pdp11-aout
ARG ARG_PREFIX=/usr/local

ENV TARGET=$ARG_TARGET
ENV PREFIX=$ARG_PREFIX
ENV PATH=$PREFIX/bin:$PATH

ENV BINUTILES_VER=2.45
ENV GCC_VER=15.1.0

# Install packages
ENV DEBIAN_FRONTEND=noninteractive

# https://github.com/moby/buildkit/issues/1662#issuecomment-683962222
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,sharing=locked,target=/var/lib/apt \
    apt-get update \
    && apt-get install --no-install-recommends -y \
    # build-essential bison flex texinfo wget curl \
    build-essential wget ca-certificates \
    libgmp-dev libmpfr-dev libmpc-dev

WORKDIR /build

# --- Build binutils ---
RUN wget https://sourceware.org/pub/binutils/releases/binutils-$BINUTILES_VER.tar.gz && \
    tar xf binutils-$BINUTILES_VER.tar.gz && \
    mkdir binutils-build && cd binutils-build && \
    ../binutils-$BINUTILES_VER/configure --target=$TARGET --prefix=$PREFIX --disable-nls && \
    make -j$(nproc) && make install

# --- Build GCC ---
RUN wget https://sourceware.org/pub/gcc/releases/gcc-$GCC_VER/gcc-$GCC_VER.tar.gz && \
    tar xf gcc-$GCC_VER.tar.gz && \
    mkdir gcc-build && cd gcc-build && \
    ../gcc-$GCC_VER/configure --target=$TARGET --prefix=$PREFIX \
    # --without-headers --enable-languages=c --disable-nls && \
    --enable-languages=c --disable-nls --disable-shared --disable-libssp --disable-libgfortran --disable-libobjc && \
    # --enable-languages=c --disable-nls --disable-libssp --disable-libgfortran --disable-libobjc && \
    make -j$(nproc) && make install
# make -j$(nproc) all-target-libgcc && make install-target-libgcc

# Stage 2
FROM ubuntu:latest

# Install packages
ENV DEBIAN_FRONTEND=noninteractive

ENV TARGET=$ARG_TARGET
ENV PREFIX=$ARG_PREFIX
ENV PATH=$PREFIX/bin:$PATH

COPY --from=builder $PREFIX $PREFIX

# Set locale and timezone
ENV LANG=ja_JP.UTF-8
ENV LC_ALL=ja_JP.UTF-8
ENV LC_CTYPE=ja_JP.UTF-8
ENV TZ=Asia/Tokyo

ARG USERNAME=vscode
ARG UID=10000
ARG GID=$UID

# Setup user and group id
# Remove all general users and create a new user for USER direction.
RUN set -eux; \
    for i in $(awk -F: '$3 >= 1000 && $3 <= 60000 { print $1 }' /etc/passwd); do \
    userdel $i; \
    done; \
    for i in $(awk -F: '$3 >= 1000 && $3 <= 60000 { print $1 }' /etc/passwd); do \
    groupdel $i; \
    done; \
    rm -rf /home/*; \
    groupadd --gid "${GID}" "${USERNAME}"; \
    useradd --uid "${UID}" --gid "${GID}" -s /bin/bash -m "${USERNAME}"

# Enable sudo
# RUN --mount=type=cache,target=/var/cache/apt \
#     --mount=type=cache,sharing=locked,target=/var/lib/apt \
#     apt-get update \
#     && apt-get install -y sudo \
#     && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
#     && chmod 0440 /etc/sudoers.d/$USERNAME

# https://github.com/moby/buildkit/issues/1662#issuecomment-683962222
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,sharing=locked,target=/var/lib/apt \
    apt-get update \
    && apt-get install --no-install-recommends -y \
    # Basic tools
    # ssh is required to handle GitHub in the container
    git ssh make less file ca-certificates \
    libgmp-dev libmpfr-dev libmpc-dev \
    python3 python3-dev python3-venv python-is-python3 \
    # System tools
    locales tzdata \
    # Configure locale
    && locale-gen ja_JP.UTF-8 \
    && update-locale LANG=ja_JP.UTF-8 \
    # Configure timezone
    && ln -fs /usr/share/zoneinfo/Asia/Tokyo /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata

# Default user
USER vscode

# COPY requirements.txt .
# ARG PIP_CACHE_DIR=/home/vscode/.cache/pip
# RUN mkdir -p $PIP_CACHE_DIR
# RUN --mount=type=cache,target=/home/vscode/.cache/pip \
#     sudo chown vscode:vscode /home/vscode/.cache/pip \
#     && python3 -m venv $HOME/venv \
#     && $HOME/venv/bin/pip install --upgrade pip \
#     && $HOME/venv/bin/pip install -r requirements.txt

# # activate venv
# RUN cat <<'EOF' >> /home/vscode/.bashrc

# export LANG=$LANG

# if [ -f "$HOME/venv/bin/activate" ] && [ -z "$VIRTUAL_ENV" ]; then
#     . "$HOME/venv/bin/activate"
# fi
# EOF
