# start by pulling the python image
FROM python:3.10

RUN mkdir /app

# switch working directory
WORKDIR /app

# copy the requirements file into the image
ADD ./app/requirements.txt /app

# install the dependencies and packages in the requirements file
RUN pip3 install -r requirements.txt

# copy every content from the local file to the image
ADD ./app /app

EXPOSE 5000

# # configure the container to run in an executed manner
ENTRYPOINT [ "python3", "app.py" ]
