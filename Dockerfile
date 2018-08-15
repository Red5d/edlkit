MAINTAINER Red5d

FROM alpine:latest

WORKDIR /usr/src/app

COPY . .

RUN apk add --no-cache py3-numpy py3-pillow py3-requests mediainfo && python3 ./setup.py install

RUN python3 -c "import imageio; imageio.plugins.ffmpeg.download()"

WORKDIR /edit

ENTRYPOINT ["edledit"]
