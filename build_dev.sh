bc=$(buildah from docker.io/library/archlinux)
buildah run $bc pacman --noconfirm -Syy
buildah run $bc pacman --noconfirm -S npm uvicorn python-fastapi python-pydantic
#buildah run $bc npm create -y vite@latest bjorligames -- --template react
#buildah run --workingdir=/bjorligames $bc npm install

buildah commit $bc react-dev
buildah rm $bc
