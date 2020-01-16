# temporary image to build der-ascii
FROM golang:latest AS build
RUN go get github.com/google/der-ascii/cmd/...

# main gringotts image
FROM python:3

# install der-ascii binaries
COPY --from=build /go/bin/ascii2der /bin/
COPY --from=build /go/bin/der2ascii /bin/

# install python dependencies
WORKDIR /app
ADD requirements.txt .
RUN apt-get update \
 && apt-get install -y libgmp-dev libmpfr-dev libmpc-dev openssl \
 && pip install --upgrade pip \
 && pip install -r requirements.txt

# add all files
ADD . .

CMD ["/app/scripts/mint.sh"]
