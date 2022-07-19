FROM python:3.9-slim-buster

RUN apt-get update \
	&& apt-get install -y gcc libmariadb-dev \
	&& apt-get clean  \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock gunicorn.conf.py ./
COPY kibune ./kibune

RUN pip install -U --no-cache-dir pip==22.1.2 \
	&& pip install --no-cache-dir poetry==1.1.14 \
	&& poetry config virtualenvs.create false \
	&& poetry install --no-dev

EXPOSE $PORT

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "kibune.main:app"]

