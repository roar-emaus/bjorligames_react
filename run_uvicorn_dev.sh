podman run -it --rm --network=host --workdir=/bjorligames -v $(pwd):/bjorligames localhost/react-dev:latest python api.py --data_path=/bjorligames/data/
