FROM node:14.18.3-bullseye

ENV WORK_DIR /opt/app
WORKDIR ${WORK_DIR}

COPY src ${WORK_DIR}/src
COPY package.json .proxyrc.json ${WORK_DIR}/

RUN set -eux ; \
    npm i

CMD ["npm", "run", "dev"]