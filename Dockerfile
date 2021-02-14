FROM ubuntu:20.10

ENV LTS_MAJOR_VERSION 2.83
ENV LTS_MINOR_VERSION 9

RUN apt-get update && apt-get install -y \ 
	curl \ 
	libopenexr-dev \ 
	bzip2 \ 
	build-essential \ 
	zlib1g-dev \ 
	libxmu-dev \ 
	libxi-dev \ 
	libxxf86vm-dev \ 
	libfontconfig1 \ 
	libxrender1 \ 
	libgl1-mesa-glx \
	apt-utils \
	python3-pip \
	&& rm -rf /var/lib/apt/lists/*

RUN curl -OL https://download.blender.org/release/Blender${LTS_MAJOR_VERSION}/blender-${LTS_MAJOR_VERSION}.${LTS_MINOR_VERSION}-linux64.tar.xz

RUN tar -xf blender-${LTS_MAJOR_VERSION}.${LTS_MINOR_VERSION}-linux64.tar.xz \
	&& rm blender-${LTS_MAJOR_VERSION}.${LTS_MINOR_VERSION}-linux64.tar.xz \
	&& mv blender-${LTS_MAJOR_VERSION}.${LTS_MINOR_VERSION}-linux64 blender

COPY ["src/blender scripts", "blender_scripts/"]
COPY src/utils blender_scripts/utils
COPY container_requirements.txt blender_scripts/requirements.txt
RUN python3 -m pip install -r blender_scripts/requirements.txt
RUN ln -s /blender/blender /usr/bin/blender
WORKDIR /blender_scripts

CMD ["python3", "main.py"]