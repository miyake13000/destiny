FROM httpd
WORKDIR /usr/local/apache2
COPY ./conf/httpd.conf ./conf/httpd.conf
RUN apt update
RUN apt install -y ruby sqlite3
CMD ["httpd-foreground"]
