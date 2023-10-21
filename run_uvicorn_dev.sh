podman run -it --rm --network=host --workdir=/bjorligames -v $(pwd):/bjorligames localhost/react-dev:latest uvicorn --reload api:app
