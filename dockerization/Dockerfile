# Use official Miniconda3 image
FROM continuumio/miniconda3:latest

# Set working directory
WORKDIR /app

# Copy your conda environment file
COPY app/quarto.yaml /app/

# Ensure conda is available in non-login shells
SHELL ["/bin/bash", "-c"]

# Install basics first
RUN apt-get update && apt-get install -y \
    vim \
    less \
    && rm -rf /var/lib/apt/lists/*

# Create conda environment from YAML file with explicit name
RUN conda env create -f quarto.yaml -n quarto

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "quarto", "/bin/bash", "-c"]

# Activate the environment by default when container starts
RUN echo "conda activate quarto" >> ~/.bashrc

# Set the environment as default for subsequent RUN commands
ENV CONDA_DEFAULT_ENV=quarto
ENV PATH /opt/conda/envs/quarto/bin:$PATH

# Default command - starts with the environment activated
CMD ["conda", "run", "-n", "quarto", "bash"]