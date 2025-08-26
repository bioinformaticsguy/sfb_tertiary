# Start from a lightweight Linux base
FROM ubuntu:22.04

# Set working directory
WORKDIR /app

# Install dependencies for conda
RUN apt-get update && apt-get install -y \
    wget \
    vim \
    bzip2 \
    ca-certificates \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy local file into image
COPY app/quarto.yaml /app/

# Download and install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -b -p /opt/conda \
    && rm /tmp/miniconda.sh

# Add conda to PATH
ENV PATH=/opt/conda/bin:$PATH

# Create a conda environment from a YAML (optional)
# COPY environment.yml .
# RUN conda env create -f environment.yml

# Activate conda environment by default (optional)
SHELL ["conda", "run", "-n", "base", "/bin/bash", "-c"]

# Default command
CMD ["bash"]
