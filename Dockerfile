FROM php:5-apache-jessie

LABEL Author="Virink <virink@outlook.com>"
LABEL Blog="https://www.virzz.com"

COPY easy_laravel/ /var/www/html/

WORKDIR /var/www/html

RUN ls -al /var/www/html && ls -al .

RUN php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');" && \
	php composer-setup.php --install-dir=/usr/local/bin && \
	mv /usr/local/bin/composer.phar /usr/local/bin/composer && \
	php -r "unlink('composer-setup.php');" && \
	composer install && \
	# composer install && \
	php artisan