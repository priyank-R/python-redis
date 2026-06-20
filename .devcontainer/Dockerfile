FROM python:3.14.3-slim-bookworm

# Basic, commonly-needed tools for a comfortable dev shell.
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    procps \
    less \
    redis-server \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user so files created in the container
# aren't owned by root on your host filesystem.
ARG USERNAME=vscode
RUN useradd -ms /bin/bash $USERNAME

USER $USERNAME
WORKDIR /workspace

# Copy project source into the image. 
COPY --chown=$USERNAME:$USERNAME . /workspace
