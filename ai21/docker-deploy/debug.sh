#!/bin/bash

SCRIPT_DIR="$( cd -- "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 ; pwd -P )"

pushd $SCRIPT_DIR/..
docker build -t riv-deploy ../images/cdk-deploy
docker run -it -v ~/.aws:/root/.aws -v `pwd`:/files -v /var/run/docker.sock:/var/run/docker.sock -w /files -p 8501:8501 --entrypoint bash riv-deploy

popd