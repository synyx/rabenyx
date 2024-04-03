FROM docker.io/library/python:3.8-slim-bullseye as base

FROM base as builder

# Install dependencies for building python dependencies
RUN apt-get update \
 && apt-get install -y libmariadb-dev gcc

# We install the application dependencies in this directory
WORKDIR /install

# First install the dependencies, so if they don't change, no new layers are created
COPY requirements.txt /install
RUN pip3 install --no-cache-dir --prefix=/install -r requirements.txt

FROM base

# Install tini, a mini-init to run forking applications in and runtime dependencies
RUN apt-get update \
 && apt-get install -y tini locales libmariadb3 \
 && echo 'de_DE.UTF-8 UTF-8' > /etc/locale.gen \
 && locale-gen \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# We run the application from this directory
WORKDIR /app

# Add all the other files to /app
COPY --from=builder /install /usr/local
COPY ./ /app

EXPOSE 5000

# Setup localization
ENV LANG="de_DE.UTF-8" TZ="Europe/Berlin"
# Setup flask
ENV FLASK_APP=webapp/app.py FLASK_ENV=production
# XXX: Runtime environment different from dev env
ENV PYTHONPATH=/app

ENTRYPOINT ["tini", "--", "/usr/local/bin/flask"]
CMD ["run", "-h", "0.0.0.0", "-p", "5000"]

LABEL org.opencontainers.image.authors="Daniela Grammlich <grammlich@synyx.de>" \
      org.opencontainers.image.url=${CI_PROJECT_URL} \
      org.opencontainers.image.vendor="synyx GmbH & Co. KG" \
      org.opencontainers.image.title="rabenyx"
