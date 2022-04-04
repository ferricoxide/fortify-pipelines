# base image
ARG DOCKER_REGISTRY=quay.io
ARG DOCKER_IMAGE=centos/centos
ARG DOCKER_VERSION=stream8

FROM ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${DOCKER_VERSION}

COPY scripts/create_app_version.py /usr/local/bin/create_app_version.py

RUN \
    [[ $( yum list installed python3 > /dev/null 2>&1 )$? -eq 0 ]] || \
      yum install -y python3 && \
    python3 -m pip install --user --upgrade pip setuptools && \
    python3 -m pip install --user --upgrade argparse && \
    python3 -m pip install --user --upgrade datetime && \
    python3 -m pip install --user --upgrade requests

ENV SSC_APP_NAME=""
ENV SSC_URL=""
ENV SSC_USER_PASS=""
ENV SSC_USER_NAME=""
ENV SSC_APP_VERSION=""

ENTRYPOINT [ "/usr/local/bin/create_app_version.py" ]
