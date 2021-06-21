FROM httpd
WORKDIR /usr/local/apache2
COPY ./conf/httpd.conf ./conf/httpd.conf
RUN apt update
RUN apt install -y ruby sqlite3
RUN gem install bundler
COPY ./Gemfile ./Gemfile
COPY ./Gemfile.lock ./Gemfile.lock
RUN bundle install
CMD ["httpd-foreground"]
