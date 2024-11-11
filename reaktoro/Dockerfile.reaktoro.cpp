# Start from Ubuntu base image
FROM ubuntu:22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
  wget \
  build-essential \
  cmake \
  git \
  unzip \
  libssl-dev

# Install Anaconda for Reaktoro
RUN wget https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Linux-x86_64.sh -O /tmp/Anaconda3-2024.10-1-Linux-x86_64.sh && \
  bash /tmp/Anaconda3-2024.10-1-Linux-x86_64.sh -b -p /opt/conda && \
  rm /tmp/Anaconda3-2024.10-1-Linux-x86_64.sh

# Add Conda to PATH
ENV PATH="/opt/conda/bin:$PATH"

# Update Conda and add conda-forge channel
RUN conda update -n base -c defaults conda -y && \
  conda config --add channels conda-forge

# Create 'rkt' environment and install Reaktoro
RUN conda create -n rkt -c conda-forge reaktoro -y

RUN apt-get install -y libasio-dev

# Download Crow release without building tests and examples
RUN wget https://github.com/CrowCpp/Crow/releases/download/v1.2.0/Crow-1.2.0.zip -O /tmp/crow.zip && \
    unzip /tmp/crow.zip -d /tmp && rm /tmp/crow.zip && \
    cp -r /tmp/Crow-1.2.0-Darwin/include/* /usr/local/include/ && \
    rm -rf /tmp/Crow-1.2.0-Darwin

# Set up application working directory and copy files
WORKDIR /app
COPY . /app

# Build the application
RUN /bin/bash -c "source activate rkt && rm -rf build && mkdir build && cd build && \
  cmake .. && make -j$(nproc)"

# Perform the cleanup after all installations are complete
RUN rm -rf /var/lib/apt/lists/*

# Specify environment to activate on container start
ENTRYPOINT ["/bin/bash", "-c", "source activate rkt && ./build/server"]
