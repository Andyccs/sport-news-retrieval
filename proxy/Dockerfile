# You must be in the root directory of this project when building this image
FROM nginx:1.9.9

USER root

COPY UI/ /usr/share/nginx/html/
COPY proxy/sport-nginx.dev.conf /etc/nginx/nginx.conf
