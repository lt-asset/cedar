ARG UBUNTU_VERSION=22.04
FROM ubuntu:${UBUNTU_VERSION}

# Install required ubuntu packages and clean up in a single RUN to reduce image size
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN apt-get update && apt-get install -y libstdc++6
RUN apt-get install -y binutils screen vim wget git && \
    rm -rf /var/lib/apt/lists/* && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    mkdir /root/.conda && \
    bash Miniconda3-latest-Linux-x86_64.sh -b && \
    rm -f Miniconda3-latest-Linux-x86_64.sh

ENV PATH /root/miniconda3/bin:$PATH

# Setup vim configuration
RUN echo 'syntax on\nset tabstop=2\nset softtabstop=2\nset showcmd\nset showmatch\nset incsearch\nset hlsearch\nset ruler' > /root/.vimrc

# Copy git repo
ARG FUZZER_HOME="/home/code/nightly-docter-eagle/" 
WORKDIR ${FUZZER_HOME}
COPY . .
# ADD ../stanford-corenlp-full-2018-02-27 /home/code/
RUN conda update -n base -c defaults conda
RUN conda install      \
          pip=23.1.2   \
          python=3.10.12 \
	      ruamel.yaml=0.17.21 \
          networkx       \
          scikit-learn=1.3.0 \
          nose=1.3.7 \
          pyyaml=5.4.1 \
          pandas=2.1.4 \
	      numpy=1.26.4 
RUN conda clean -afy

        
CMD /bin/bash
