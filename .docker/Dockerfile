FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV WEB_CONCURRENCY 1

ARG USER_ID=1001
ARG GROUP_ID=1001
ARG WATCHMAN_VERSION="v2021.05.10.00"

# switch user
USER root

# Add netcat
RUN apt-get update && apt-get install -y \
        netcat

RUN groupadd www-user -g $GROUP_ID
RUN adduser --home "/home/www-user" --uid $USER_ID --gid $GROUP_ID www-user
ENV PATH="${PATH}:/home/www-user/.local/bin/"

# Add entrypoint
COPY ./.docker/docker-entrypoint.sh /usr/local/bin/docker-entrypoint
RUN chmod +x /usr/local/bin/docker-entrypoint

# Prepare project destination
RUN mkdir -p /opt/app-root/src
RUN chown -R www-user:www-user /opt/app-root/src

USER www-user

WORKDIR /opt/app-root/src

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY --chown=www-user:www-user . /opt/app-root/src
COPY --chown=www-user:www-user app/wsgi.py /opt/app-root/src

EXPOSE 8080

ENTRYPOINT ["docker-entrypoint"]
CMD ["/usr/libexec/s2i/run"]
