FROM python:3.9

RUN apt-get update \
 && apt-get install -y apache2 libapache2-mod-wsgi-py3 \
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
 && pip install -r requirements.txt

COPY . /npdb
RUN cp apache_django_host.conf /etc/apache2/sites-enabled/apache_django_host.conf \
 && sed -i 's/Listen 80/Listen 8080/' /etc/apache2/ports.conf \
 && chmod a+wrx /npdb \
 && chmod -R a+wrx /var/log/apache2 \
 && chmod -R a+wrx /var/run/apache2

EXPOSE 8080

ENTRYPOINT ["/npdb/entrypoint.sh"]
CMD ["/bin/bash"]
