FROM alpine:latest

# https://github.com/krallin/tini.git
RUN apk add --no-cache tini
ENTRYPOINT ["/sbin/tini", "--"]

