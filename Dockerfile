FROM ubuntu:latest

RUN apt-get update && apt-get install -y gosu
# non-root user for security
RUN addgroup appgroup && adduser -S -G appgroup appUser
USER appUser

#FROM python:3.12 AS build-image
FROM python:3.12-slim
WORKDIR /
RUN mkdir src
RUN mkdir -p function
COPY ./src /src
RUN chmod 755 /src
COPY ./requirements.txt .

RUN pip install -r /requirements.txt
# RUN pip install -r /function/requirements.txt --target /function awslambdaric

# Use a slim version of the base Python image to reduce the final image size
# FROM python:3.12-slim

# Copy in the built dependencies
# COPY --from=build-image /function /function
EXPOSE 3000

# Set runtime interface client as default command for the container runtime
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
# ENTRYPOINT [ "python3", "/src/app.py", "runserver" ]
# Pass the name of the function handler as an argument to the runtime
CMD [ "/src/app.handler" ]
