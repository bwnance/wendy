FROM python:3.12-slim

RUN apt-get update
RUN apt-get install -y ffmpeg libavcodec-extra wget nano git cron

RUN mkdir -p /usr/local/bin
COPY convert-m4a-to-mp3.sh /usr/local/bin/convert-m4a-to-mp3
RUN chmod +x /usr/local/bin/convert-m4a-to-mp3

RUN touch /var/log/cron.log

RUN pip install --upgrade poetry
WORKDIR /code
RUN git clone https://github.com/bwnance/tidal-dl-ng.git
WORKDIR /code/tidal-dl-ng
RUN poetry config --local virtualenvs.create false
RUN poetry install

WORKDIR /

RUN mkdir -p /data
RUN mkdir -p /tracks
RUN mkdir -p /sctracks

COPY tidal-cron /etc/cronjob
RUN crontab /etc/cronjob

# can't configure config path in tidal-dl-ng cleanly, so symlink the default one
RUN mkdir -p /data/config/
RUN mkdir -p /root/.config
RUN ln -s /data/config/ /root/.config/tidal_dl_ng


COPY settings.json /tmp/settings.json
COPY tidal_input.txt /tmp/tidal_input.txt
COPY sc_input.txt /tmp/sc_input.txt

RUN mkdir -p /code
COPY run.sh /code/run.sh
RUN chmod 0744 /code/run.sh
COPY setup.sh /code/setup.sh
RUN chmod 0744 /code/setup.sh
RUN chown nobody:users /data/
RUN chown nobody:users /tracks/
CMD sleep 5 && sh /code/setup.sh && tidal-dl-ng login && cron && tail -f /var/log/cron.log