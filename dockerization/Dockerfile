# Use official Ubuntu base image
FROM ubuntu:22.04

# Set working directory
WORKDIR /app

# Use bash for RUN commands
SHELL ["/bin/bash", "-c"]

# Install basics, Python 3.11, pip, and other required tools
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    tar \
    python3.11 \
    python3.11-venv \
    python3.11-distutils \
    python3-pip \
    git \
    vim \
    less \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python3.11 -m pip install --upgrade pip

# Install Pandas and Jupyter
RUN python3.11 -m pip install pandas jupyter

# Download and install Quarto (latest version)
RUN wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.7.34/quarto-1.7.34-linux-amd64.tar.gz -O /tmp/quarto.tar.gz


# Extract Quarto to /usr/local/quarto
RUN mkdir -p /usr/local/quarto && \
    tar -C /usr/local/quarto -xvzf /tmp/quarto.tar.gz --strip-components=1 && \
    rm /tmp/quarto.tar.gz

# Add Quarto to PATH
ENV PATH="/usr/local/quarto/bin:${PATH}"

# Verify installation
RUN quarto --version

# Default command
CMD ["bash"]