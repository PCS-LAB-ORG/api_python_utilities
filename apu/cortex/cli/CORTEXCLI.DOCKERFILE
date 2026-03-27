FROM ruby:latest

COPY install_cortexcli.sh .

RUN install_cortexcli.sh

RUN PATH="$PATH:$PWD"