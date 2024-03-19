FROM python:3.11-slim-buster

WORKDIR /app

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
# CMD python manage.py runserver 0.0.0.0:80
CMD gunicorn --bind 0.0.0.0:8000 ticket_management.wsgi



# Docker File For PROD
# Base image
# FROM python:3.11-slim-buster
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # create directory for the app user
# RUN mkdir -p /home/app

# # don't run as root therefore create non-root user
# RUN groupadd --gid 1001 app && \
#     useradd --uid 1001 --gid app --home /home/app app

# # install pipenv
# RUN pip install pipenv

# # create the appropriate directories
# ENV HOME=/home/app
# ENV APP_HOME=/home/app/website
# RUN mkdir $APP_HOME
# RUN mkdir $APP_HOME/staticfiles
# RUN mkdir $APP_HOME/mediafiles
# WORKDIR $APP_HOME

# # installing dependencies
# COPY Pipfile Pipfile.lock $APP_HOME

# # install dependencies
# RUN pipenv install --system

# # copy project files and directories
# COPY . $APP_HOME

# # chown all the files to the app user
# RUN chown -R app:app $APP_HOME

# # change to the app user
# USER app