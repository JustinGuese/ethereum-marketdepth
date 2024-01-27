docker container to grab latest ethereum orderbook information from binance and write to a partitioned parquet gzipped file

https://github.com/JustinGuese/ethereum-marketdepth/tree/main
https://hub.docker.com/repository/docker/guestros/binance-orderbook-getter/general

usage:

`docker-compose up -d`
& then watch ./data fill

or

`docker run -v ./data:/app/data/ --name binance-orderbook-to-parquet -d guestros/binance-orderbook-getter:latest`
