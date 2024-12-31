FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update -y && apt-get install -y --no-install-recommends python3-dev gcc libc-dev && rm -f /var/lib/apt/lists/*.
WORKDIR /test/
RUN pip install --upgrade pip
COPY ./requirements.txt /test/
RUN pip install -r requirements.txt
COPY ./library /test/library
EXPOSE 8000

