# Set base image (host OS)
# Had trouble getting cryptography to work. Had to change python build version to 3.9 from Alpine.
FROM python:3.9

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /

# Copy the dependencies file to the working directory
# This copies all existing files. I thought there was a problem
#   with the workDir or Python venv. But nope, I didnt port anything..
COPY . .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY app.py .

# Specify the command to run on container start
CMD [ "python", "./app.py" ]