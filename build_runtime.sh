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
buildah run $bc_build npm run build

# Final stage using Alpine
bc=$(buildah from docker.io/library/alpine:latest)
buildah run $bc apk add --no-cache python3 py3-pip
buildah run $bc pip3 install uvicorn[standard] fastapi pydantic gunicorn

buildah copy --from=$bc_build $bc /bjorligames_react/project/dist /bjorligames_react/project/dist
buildah copy --from=$bc_build $bc /bjorligames_react/data /bjorligames_react/data
buildah copy --from=$bc_build $bc /bjorligames_react/api.py /bjorligames_react/api.py

buildah config --workingdir=/bjorligames_react/ $bc
buildah config --env DATA_PATH=/bjorligames_react/data/ $bc

buildah config --cmd "gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app --bind 0.0.0.0:80" $bc

buildah commit $bc localhost/bjorligames:latest
buildah rm $bc $bc_build
