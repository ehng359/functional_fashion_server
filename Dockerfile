FROM python:3.10-alpine

RUN apk add --update make cmake gcc g++ gfortran
RUN apk --no-cache add musl-dev linux-headers

RUN pip3 install django django-rest-framework django-debug-toolbar cpython numpy scipy neurokit2

# Copy the current directory contents into the container at /app 
ADD . /app

# Set the working directory to /app
RUN chown -R 1000:1000 /app
USER 1000:1000
WORKDIR /app

# Setting Up Django Rest Framework
RUN python3 manage.py collectstatic
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py migrate --run-syncdb

RUN python3 manage.py makemigrations collect
RUN python3 manage.py migrate collect

RUN python3 manage.py makemigrations process_ecg
RUN python3 manage.py migrate process_ecg

VOLUME /app

EXPOSE 8000

ENTRYPOINT ["python"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]