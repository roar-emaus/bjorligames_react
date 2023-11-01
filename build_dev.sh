#!/bin/bash
set -x
set -e

# Build stage using Alpine
bc_build=$(buildah from docker.io/library/alpine:latest)
buildah run $bc_build apk add --no-cache git npm python3 py3-pip
buildah run $bc_build pip3 install uvicorn[standard] fastapi pydantic gunicorn

buildah run $bc_build git clone https://github.com/roar-emaus/bjorligames_react.git
buildah config --workingdir=/bjorligames_react/project $bc_build
buildah run $bc_build npm install
buildah commit $bc_build localhost/bjorligames-dev
buildah rm $bc_build
