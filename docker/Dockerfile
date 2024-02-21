# Use the official Python base image
FROM python:3.11
LABEL authors="grafuls"

RUN apt-get install git patch

# Set the working directory inside the container
WORKDIR /opt
RUN git clone https://github.com/redhat-performance/wppt
WORKDIR /opt/wppt

# Install Poetry
RUN pip install poetry

# Install project dependencies
RUN make install

# Set the entrypoint command to run the project
CMD ["make", "run",]
