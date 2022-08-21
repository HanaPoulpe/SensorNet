FROM python:3.10

# Install SensorNet
COPY ./ src/
RUN python -m pip install -U pip
WORKDIR "/src"
RUN pip install -r build_requirements.txt
RUN tox
WORKDIR "/src/.tox/dist"
RUN pip install $(ls .)

# Clean up
WORKDIR "/"
RUN rm -Rf /src
