#!/bin/sh

certbot certonly --standalone  -n --agree-tos --expand -d $1 --email $2
/usr/sbin/nginx -g "daemon off;"
/usr/sbin/crond -f -d 8 &
