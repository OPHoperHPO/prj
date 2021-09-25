FROM ethereum/client-go

ARG ACCOUNT_PASSWORD
ARG INIT
ARG ACCOUNT
COPY Genesis.json /tmp

RUN if [[ -z "$INIT" ]]; then geth init /tmp/Genesis.json; fi

RUN if [[ -z "$INIT" ]]; then rm -f ~/.ethereum/geth/nodekey; fi

RUN if [[ -z "$ACCOUNT" ]]; then echo somthing; else echo ${ACCOUNT_PASSWORD} > /tmp/password && geth account new --password /tmp/password && rm -f /tmp/password; fi

