# docker build -t pyavplayground pyav-playground/ && docker image prune -f
# docker run -it pyavplayground /bin/bash
FROM ubuntu:latest
WORKDIR /data
COPY . /data
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install pkg-config python3.10 python3-pip libavformat-dev libavcodec-dev \
libavdevice-dev libavutil-dev libswscale-dev libswresample-dev libavfilter-dev -y
RUN pip3 install --upgrade -r PyAV/tests/requirements.txt
RUN pip3 install cython==0.29.37
RUN cd PyAV
RUN python3 setup.py build
RUN python3 setup.py install
RUN pip3 install klvdata opencv-python
ENV PYTHONPATH /usr/local/lib/python3.10/dist-packages
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENTRYPOINT ["python3 PyAV/setup.py install"]
