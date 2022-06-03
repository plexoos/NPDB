FROM python:3.9

RUN apt-get update \
 && apt-get install -y apache2 libapache2-mod-wsgi-py3 \
 && apt-get install -y nginx \
 && rm -rf /var/lib/apt/lists/*

RUN a2enmod wsgi rewrite proxy_http \
 && a2enmod proxy proxy_http proxy_balancer lbmethod_byrequests \
 && a2dissite 000-default

# Ensure that the python output is sent straight to terminal
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /npdb
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# We copy this source dir after establishing the python environment in order to
# avoid re-installation of pip modules while developing the app
COPY . /npdb

RUN chmod -R 775 /npdb

RUN cp apache_django_host.conf /etc/apache2/sites-enabled/ \
 && sed -i 's/Listen 80/Listen 8080/' /etc/apache2/ports.conf \
 && chmod -R 777 /var/log/apache2 \
 && chmod -R 775 /var/run/apache2

RUN cp nginx_django_host.conf /etc/nginx/conf.d/ \
 && chmod -R 777 /var/log/nginx \
 && chmod -R 775 /var/lib/nginx \
 && mkdir -p -m 775 /var/run/nginx

EXPOSE 8080

ENTRYPOINT ["/npdb/entrypoint.sh"]
CMD ["/bin/bash"]
