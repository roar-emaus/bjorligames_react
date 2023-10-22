podman run -it \
 --rm \
 --network=host \
 --workdir=/bjorligames/data \
 -v $(pwd):/bjorligames \
 localhost/react-dev:latest redis-server --port 6379 --dir /bjorligames/data/ --dbfilename dump.rdb
