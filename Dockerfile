ARG IMAGE_NAME
ARG IMAGE_VERSION

FROM ${IMAGE_NAME}:${IMAGE_VERSION}

WORKDIR /opt/dendroid

COPY pyproject.toml .
COPY README.md .
COPY setup.py .
COPY dendroid dendroid
COPY tests tests

RUN pip install -e .[tests]
