FROM python:3.9-alpine

RUN pip3 install django django-rest-framework django-debug-toolbar

# Copy the current directory contents into the container at /app 
ADD . /app

# Set the working directory to /app
RUN chown -R 1000:1000 /app
USER 1000:1000
WORKDIR /app

RUN python3 manage.py createsuperuser
RUN python3 manage.py collectstatic
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py migrate --run-syncdb

VOLUME /app

EXPOSE 8000

ENTRYPOINT ["python"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]