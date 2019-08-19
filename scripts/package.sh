#!/usr/bin/env bash

set -eu

main(){
  zip Golang.sublime-package go/*.py
  zip -j Golang.sublime-package scripts/dev.py
  zip -j Golang.sublime-package conf/*
}

main
