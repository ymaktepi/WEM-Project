#! /bin/bash

function build_and_start
{
    local readonly PATH_TO_SCRIPT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    pushd $PATH_TO_SCRIPT
    python setup.py sdist
    cp dist/*.tar.gz application/
    docker-compose up --build
    popd 
}

build_and_start
