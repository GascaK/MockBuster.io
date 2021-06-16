# MockBuster.io
## Your personal movie database.

![Docker Cloud Automated build](https://img.shields.io/docker/cloud/automated/gascak/mbuster) [![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger) ![GitHub language count](https://img.shields.io/github/languages/count/GascaK/MockBuster.io) ![Website](https://img.shields.io/website?down_color=lightgrey&down_message=offline&up_color=blue&up_message=online&url=https%3A%2F%2Fmockbuster.io)

Have boxes in your garage full of old DVD or VHS tapes? Run out of space in your tv stand but want to know what movies are in storage? Add all your dvd/vhs movie titles and keep a record of them online!

## Features
- Free storage of unlimited movie titles
- Simple User Interface to add all your movies quickly.
- Absolutely free.
#
#
## Testimonials
> This is so cool. I've never seen my name
> written like that.
>          -My wife

> So you made a fake blockbuster?
> -Mom

#
#

## Tech

Mockbuster employs a variety of tech

- [Javascirpt] - HTML enhanced for web apps!
- [Python] - awesome web-based text editor
- [CSS] - make things look great
- [Bootstrap] - great UI boilerplate for modern web apps
- [jQuery] - evented I/O for the backend
#
#

## Docker

MockBuster uses docker images hosted on lightsail containers. Hosted on [dockerhub](https://hub.docker.com/repository/docker/gascak/mbuster)

Install the dependencies and devDependencies and start the server.

```
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
```

## Development
Want to contribute? Awesome. Please check out the issues tab for further.

## License

MIT

**Free Software, Hell Yeah!**
