FROM python:3.10

# Install SensorNet
COPY .tox/dist /dist
RUN python -m pip install -U pip
RUN pip install /dist/$(ls /dist)
