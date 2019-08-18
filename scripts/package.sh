#!/usr/bin/env bash

set -eu

main(){
  zip -j go.sublime-package src/go/*.py
  zip -j go.sublime-package conf/*
}

main
