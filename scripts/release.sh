#!/usr/bin/env bash

set -eu

main(){
  local tag="$(git tag --points-at HEAD)"

  if test $tag; then
    echo "==> packaging"
    scripts/package.sh
    echo "==> releasing"
    ghr --soft $tag go.sublime-package
    echo "==> released $tag"
    return 0
  fi

  echo "==> not a release"
  return 1
}

main $@
