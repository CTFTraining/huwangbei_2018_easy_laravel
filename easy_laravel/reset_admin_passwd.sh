#!/bin/sh
while true; do
	# reset passwd
	php /usr/local/bin/reset_admin_passwd
	# reset template
	cp /var/www/html/storage/flag.php /var/www/html/storage/framework/views/73eb5933be1eb2293500f4a74b45284fd453f0bb.php
	touch -t 209911111111.11 /var/www/html/storage/framework/views/73eb5933be1eb2293500f4a74b45284fd453f0bb.php
	sleep 3m
done