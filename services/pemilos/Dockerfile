FROM python:3.9-alpine

RUN pip install --no-cache-dir pipenv

# 1. Install dependencies

WORKDIR /usr/src/pemilos

COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

# 2. Copy files

WORKDIR /usr/src/pemilos

COPY . .

# 3. Container configurations

EXPOSE 8000

ENTRYPOINT [ "sanic" ]
CMD [ "--host", "0.0.0.0", "main.app" ]
