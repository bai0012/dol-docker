FROM nginx:alpine-slim

COPY apps /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

VOLUME /etc/nginx/ssl
VOLUME /etc/nginx/auth

EXPOSE 8443

CMD ["sh", "-c", "nginx -g 'daemon off;'"]
