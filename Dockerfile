# Set base image (host OS)
# Had trouble getting cryptography to work. Had to change python build version to 3.8 from Alpine.
FROM python:3.8

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
# RUN apt-get update \
#     && apt-get install -y --no-install-recommends gcc and-build-dependencies \
#     && rm -rf /var/lib/apt/lists/* \
#     && pip install cryptography \
#     && apt-get purge -y --auto-remove gcc and-build-dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY app.py .

# Specify the command to run on container start
CMD [ "python", "./app.py" ]