# set base image (host OS)
FROM python:3.9.5-slim-buster

# set the working directory in the container
WORKDIR /app

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies to the local user directory (eg. /root/.local)
RUN pip install --user -r requirements.txt

# copy the content of the local src directory to the working directory
COPY ./src/ .

# command to run on container start
CMD [ "python", "./app.py" ]