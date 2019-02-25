FROM python:3.6
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install pipenv
RUN pipenv install --system --dev --ignore-pipfile
WORKDIR /app/cereal
RUN python manage.py collectstatic --noinput
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
